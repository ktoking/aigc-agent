package com.shopee.banking.uc.app.service.app.impl.login;

import com.google.common.collect.Lists;
import com.shopee.banking.sg.toolbox.crypt.CryptUtils;
import com.shopee.banking.sg.toolbox.crypt.DataTypeEnum;
import com.shopee.banking.sg.toolbox.crypt.EncryptData;
import com.shopee.banking.sg.toolbox.log.LogMasker;
import com.shopee.banking.uc.app.bo.AllClientInfoBO;
import com.shopee.banking.uc.app.bo.CertDTO;
import com.shopee.banking.uc.app.bo.CommonRiskRequestDTO;
import com.shopee.banking.uc.app.bo.LoginRiskDTO;
import com.shopee.banking.uc.app.constant.Constants;
import com.shopee.banking.uc.app.constant.LoginType;
import com.shopee.banking.uc.app.constant.UCOperationSceneEnum;
import com.shopee.banking.uc.app.converter.RiskDTOConverter;
import com.shopee.banking.uc.app.risk.framework.GenericRiskContext;
import com.shopee.banking.uc.app.risk.framework.RiskAction;
import com.shopee.banking.uc.app.risk.framework.RiskCacheContext;
import com.shopee.banking.uc.app.service.app.AppUserService;
import com.shopee.banking.uc.app.service.inside.BankCoreService;
import com.shopee.banking.uc.infra.common.ChannelTypeEnum;
import com.shopee.banking.uc.infra.common.Common;
import com.shopee.banking.uc.infra.common.CommonConstant;
import com.shopee.banking.uc.infra.common.UserStatusEnum;
import com.shopee.banking.uc.infra.common.UserTagEnum;
import com.shopee.banking.uc.infra.config.InfraApolloConfig;
import com.shopee.banking.uc.infra.constant.SubUserStatusEnum;
import com.shopee.banking.uc.infra.constant.UserTypeEnum;
import com.shopee.banking.uc.infra.dal.AppSubUserInfoDAO;
import com.shopee.banking.uc.infra.dal.AppUserInfoDAO;
import com.shopee.banking.uc.infra.dto.AppSubUserInfoDO;
import com.shopee.banking.uc.infra.dto.AppUserInfoDO;
import com.shopee.banking.uc.infra.dto.OneTimeDO;
import com.shopee.banking.uc.infra.exception.BizErrorType;
import com.shopee.banking.uc.infra.exception.BizException;
import com.shopee.banking.uc.infra.sal.ekyc.EkycApi;
import com.shopee.banking.uc.infra.sal.risk.dto.RiskAccessResDO;
import com.shopee.banking.uc.infra.sal.risk.dto.UserRiskConfigDO;
import com.shopee.banking.uc.infra.utils.AppUpdateErrorCodeUtil;
import com.shopee.banking.uc.infra.utils.BankRequestContext;
import com.shopee.banking.uc.infra.utils.VersionUtil;
import com.shopee.bcf.common.pojo.Result;
import com.shopee.bcf.common.util.JacksonUtil;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections.CollectionUtils;
import org.apache.commons.lang3.StringUtils;
import org.apache.logging.log4j.util.Strings;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;


/**
 * @author winray
 * @email wenrui.liu@shopee.com
 * @since 2024/4/11
 */
@Slf4j
@RiskAction(finishSelf = true, scene = UCOperationSceneEnum.LOGIN)
public class AppUserLoginService extends AbstractLoginService {

    @Autowired
    private AppUserInfoDAO appUserInfoDAO;

    @Autowired
    private AppSubUserInfoDAO appSubUserInfoDAO;

    @Autowired
    private BankCoreService bankCoreService;

    @Autowired
    private InfraApolloConfig apolloConfig;

    @Autowired
    private AppUserService appUserService;

    @Autowired
    private EkycApi ekycApi;


    @Override
    public Result<?> afterRiskAccess(GenericRiskContext context, RiskAccessResDO response) {
        if (Common.FLOW_BEGIN.equals(context.getStep())) {
            LoginRiskDTO loginRiskDTO = context.getRiskRequest(LoginRiskDTO.class);
            checkChildAccountLoginSupported(loginRiskDTO.getUid());
        }
        UserRiskConfigDO config = apolloConfig.getSdkMappingConfig().get(context.getRiskScene().name());
        if (Objects.equals(response.getStep(), Common.JUMP_APP_STEP)
                && config != null
                && Strings.isNotEmpty(config.getMappingScene())) {
            response.getRdExtraInfo().put(Common.DEEP_LINK_NAME, config.getDeepLinkUrl() + response.getTranId());
        }
        return super.afterRiskAccess(context, response);
    }

    /**
     * Child accounts can only log in through a supported MariBank App version.
     * The check runs after the BE risk response and before token issuance.
     *
     * @param shareUid resolved ShareUID
     */
    protected void checkChildAccountLoginSupported(Long shareUid) {
        AppUserInfoDO userInfoDO = userCacheService.getUserInfo(shareUid);
        if (userInfoDO == null || !Objects.equals(CommonConstant.CHILD_CUSTOMER_TAG, userInfoDO.getCustomerTag())) {
            return;
        }

        String channel = BankRequestContext.getChannel();
        if (!StringUtils.equals(ChannelTypeEnum.APP.getChannel(), channel)) {
            log.info("Child account login is rejected for unsupported channel, shareUid:{}, channel:{}", shareUid, channel);
            throw BizErrorType.APP_NEED_UPDATE_IN_SDK.wrap();
        }

        String appVersion = BankRequestContext.getAppVersion();
        String minAppVersion = apolloConfig.getChildAccountLoginMinAppVersion();
        if (StringUtils.isAnyBlank(appVersion, minAppVersion) || !checkVersion(appVersion, minAppVersion)) {
            log.info("Child account login requires app update, shareUid:{}, appVersion:{}, minAppVersion:{}",
                    shareUid, appVersion, minAppVersion);
            throw BizErrorType.APP_NEED_UPDATE.wrap();
        }
    }

    @Override
    public Result<?> beforeRiskAccess(GenericRiskContext context) {
        Result<?> beforeRes = doBeforeRiskAccess(context);
        if (Objects.nonNull(beforeRes)) {
            return beforeRes;
        }

        Result<?> res = super.beforeRiskAccess(context);

        // 若用户存在一次性标签则返回
        LoginRiskDTO dto = (LoginRiskDTO) res.getData();
        AppUserInfoDO infoDO = userCacheService.getUserInfo(dto.getUid());
        if (infoDO != null && !Objects.equals(infoDO.getTag(), UserTagEnum.NONE.getCode())) {
            log.info("[login] user had one time tag uid:{} tag:{}", dto.getUid(), infoDO.getTag());
            if(Objects.equals(infoDO.getTag(), UserTagEnum.DUMMY.getCode())){
                throw new BizException(BizErrorType.COMMON_APP_ERROR);
            }
            OneTimeDO oneTimeDO = new OneTimeDO();
            oneTimeDO.setOneTimeDO(infoDO);
            String appVersion = BankRequestContext.getAppVersion();
            String maskFiledVersion = apolloConfig.getMaskFiledVersion();
            if (!StringUtils.isAnyBlank(appVersion, maskFiledVersion) && checkVersion(appVersion, maskFiledVersion)) {
                oneTimeDO.setPhone(VersionUtil.phoneMask(oneTimeDO.getPhone()));
            }
            return Result.success(oneTimeDO);
        }

        return res;
    }

    /**
     * 校验请求中的appver是否大于等于配置的appver
     *
     * @param reqAppver
     * @param cfgAppver
     * @return
     */
    private boolean checkVersion(String reqAppver, String cfgAppver) {
        try {
            return VersionUtil.compare(reqAppver, cfgAppver) >= 0;
        } catch (Exception e) {
            log.error("Error occurred while comparing versions，reqAppVersion:{},cfgMinAppVersion:{}", reqAppver, cfgAppver, e);
        }
        return false;
    }

    protected Result<?> doBeforeRiskAccess(GenericRiskContext context) {
        LoginRiskDTO loginRiskDTO = context.getRiskRequest(LoginRiskDTO.class);
        if (Common.FLOW_BEGIN.equals(context.getStep())) {
            //获取登录sharedUid
            Long uid = getActiveShareUid(loginRiskDTO);
            loginRiskDTO.setUid(uid);
            checkPasswordLoginSupported(loginRiskDTO, uid);

            //获取sharedUser的所有子user列表和CIF客户列表
            AllClientInfoBO allClientInfoResp = bankCoreService.getAllClientInfoList(uid);
            log.info("getAllClientInfoList:{}", LogMasker.toJSON(allClientInfoResp));

            //获取目标登录subUid
            selectSubUserToLogin(loginRiskDTO, allClientInfoResp);

            //设置loginType进入风险识别的bizExtInfo
            LoginType loginTypeEnum = LoginType.getByCode(loginRiskDTO.getLoginType());
            Map<String, Object> biz = Optional.ofNullable(loginRiskDTO.getBizExtInfo()).orElse(new HashMap<>(4));
            biz.put(Constants.LOGIN_TYPE, loginTypeEnum.getCode());
            loginRiskDTO.setBizExtInfo(biz);
        } else {
            //从缓存中取出bizExtInfo
            RiskCacheContext cacheContext = genericCacheApi.doubleGet(loginRiskDTO.getTranId(), RiskCacheContext.class);
            if (cacheContext == null) {
                log.error("RiskContext is null from cache.tranId:{}", loginRiskDTO.getTranId());
                throw BizErrorType.SESSION_TIMEOUT.wrap();
            }
            //从缓存中取出paramInfo
            if (cacheContext.getParamInfo() != null) {
                loginRiskDTO.setParamInfo(JacksonUtil.parseObject(cacheContext.getParamInfo(), CertDTO.class));
            }

        }
        return null;
    }

    protected void checkPasswordLoginSupported(LoginRiskDTO loginRiskDTO, Long shareUid) {
        if (Boolean.FALSE.equals(apolloConfig.isLoginCheckPwdForceUpdateEnabled())) {
            return;
        }
        if (StringUtils.equals(ChannelTypeEnum.SDK.getChannel(), BankRequestContext.getChannel())) {
            return;
        }
        if (!LoginType.PASSWORD.getCode().equals(loginRiskDTO.getLoginType())) {
            return;
        }
        String loginTypes = riskClientApi.getSupportLoginTypesV3(shareUid);
        if (StringUtils.isBlank(loginTypes)) {
            log.info("Password login is not supported, shareUid:{}, loginTypes:{}", shareUid, loginTypes);
            AppUpdateErrorCodeUtil.throwException();
            return;
        }
        if (Lists.newArrayList(StringUtils.split(loginTypes, ",")).contains(LoginType.PASSWORD.getCode())) {
            return;
        }
        log.info("Password login is not supported, shareUid:{}, loginTypes:{}", shareUid, loginTypes);
        AppUpdateErrorCodeUtil.throwException();
    }

    @Override
    protected RiskCacheContext convertRiskContextInBeStep(CommonRiskRequestDTO commonRiskRequest) {
        if (commonRiskRequest instanceof LoginRiskDTO) {
            return RiskDTOConverter.INSTANCE.toCacheContext((LoginRiskDTO) commonRiskRequest);
        }
        log.error("commonRiskRequest not instance LoginRiskDTO.{}", LogMasker.toJSON(commonRiskRequest));
        return super.convertRiskContextInBeStep(commonRiskRequest);
    }

    @Override
    protected void afterLogin(LoginRiskDTO reqDTO, Exception ex) {
        saveLoginLogToEs(reqDTO, ex);

        Result<Void> result;

        if (ex instanceof BizException) {
            //业务异常
            result = Result.fail(((BizException) ex).getErrorType());
        } else if (ex != null) {
            //其他异常
            result = Result.fail(BizErrorType.SYS_ERROR);
        } else {
            //正常
            result = Result.success();
        }
        reportAntiFraud(reqDTO, ex == null, result);
    }

    protected BizErrorType uidNotFoundError() {
        return BizErrorType.USER_NO_FOUND;
    }

    protected BizErrorType statusInvalidError() {
        return BizErrorType.STATUS_ERROR;
    }

    /**
     * 根据加密UID或者手机号获取正常用户状态的明文uid
     *
     * @param loginReqDTO
     * @return 明文uid
     */
    protected Long getActiveShareUid(LoginRiskDTO loginReqDTO) {
        Long shareUid;
        //从加密uid获取客户uid
        if (StringUtils.isNotBlank(loginReqDTO.getEncryUid())) {
            try {
                shareUid = Long.valueOf(authorizationCenterApi.decrypt(loginReqDTO.getEncryUid()));
            } catch (Exception e) {
                log.error("Error happen while decrypt shareUid.", e);
                throw new BizException(BizErrorType.UID_DECRYPT_ERROR);
            }
            AppUserInfoDO userInfoDO = userCacheService.getUserInfo(shareUid);

            if (userInfoDO == null) {
                log.info("[login] user not found by encrypted shareUid loginReqDTO:{}", LogMasker.toJSON(loginReqDTO));
                throw new BizException(uidNotFoundError());
            }
            if (UserStatusEnum.INACTIVE == userInfoDO.getUserStatus()) {
                log.info("[login] no active user found by encrypted shareUid loginReqDTO:{}", LogMasker.toJSON(loginReqDTO));
                throw new BizException(statusInvalidError());
            }
            return shareUid;
        }

        //根据手机号查询uid
        if (StringUtils.isNotBlank(loginReqDTO.getCyCode()) && StringUtils.isNotBlank(loginReqDTO.getPhone())) {
            String encryptedPhone = CryptUtils.encrypt(new EncryptData(loginReqDTO.getPhone(), DataTypeEnum.PHONE_NUMBER));
            List<AppUserInfoDO> appUserInfoDOS = appUserInfoDAO.getUserInfoByPhone(loginReqDTO.getCyCode(), encryptedPhone);

            //没有用户记录
            if (CollectionUtils.isEmpty(appUserInfoDOS)) {
                log.info("[login] user not found by phone loginReqDTO:{}", LogMasker.toJSON(loginReqDTO));
                throw uidNotFoundError().wrap();
            }

            //没有active的用户记录
            AppUserInfoDO activeUserInfoDO = appUserInfoDOS
                    .stream()
                    .filter(userInfoDO -> UserStatusEnum.ACTIVE == userInfoDO.getUserStatus())
                    .findAny()
                    .<BizException>orElseThrow(() -> {
                        log.info("[login] no active user found by phone loginReqDTO:{}", LogMasker.toJSON(loginReqDTO));
                        throw statusInvalidError().wrap();
                    });

            return activeUserInfoDO.getShareUid();
        }
        //参数错误
        throw BizErrorType.PARAM_CHECK_ERROR.wrap();
    }

    /**
     * 选择子用户登录
     *
     * @param loginRiskDTO
     * @param allClientInfoResp individual & corp cif info 包括 active & inactive 状态
     */
    protected void selectSubUserToLogin(LoginRiskDTO loginRiskDTO, AllClientInfoBO allClientInfoResp) {
        //分别获取个人cif和企业cif列表
        AllClientInfoBO.CommonClient individualClientInfo = allClientInfoResp.getIndividualClientInfo();
        List<? extends AllClientInfoBO.CommonClient> corpClientInfos = allClientInfoResp.getCorpClientInfos();

        //有目标子uid的先进行登录
        if (Objects.nonNull(loginRiskDTO.getTargetEncryptedSubUid())) {
            if (setTargetSubUserFromParam(loginRiskDTO, allClientInfoResp)) {
                return;
            }
        }

        //没有开过户cif记录 登录shareUser
        if (allClientInfoResp.noCifRecords()) {
            log.info("ShareUid has not cif record.{}", loginRiskDTO.getUid());
            return;
        }

        //存在cif但是全部cif inactive,并且没有申请单 则登录异常
        if (allClientInfoResp.noneOfThemAreActive() && CollectionUtils.isEmpty(ekycApi.getOngoingApplications(loginRiskDTO.getUid()))) {
            log.info("[login] all cif client status are inactive can not login from this user uid:{},clients:{}", loginRiskDTO.getUid(), allClientInfoResp);
            throw new BizException(BizErrorType.STATUS_ERROR);
        }

        SubUserInfo subUser = getLoginSubUser(individualClientInfo, corpClientInfos);
        loginRiskDTO.setSubUid(subUser.getSubUid());
        loginRiskDTO.setUidType(subUser.getUidType());
    }

    public SubUserInfo getLoginSubUser(AllClientInfoBO.CommonClient individualClientInfo, List<? extends AllClientInfoBO.CommonClient> corpClientInfos) {
        SubUserInfo resp = new SubUserInfo();
        String channel = StringUtils.isBlank(BankRequestContext.getChannel()) ? ChannelTypeEnum.APP.getChannel() : BankRequestContext.getChannel();
        ChannelTypeEnum channelTypeEnum = ChannelTypeEnum.of(channel);
        switch (channelTypeEnum) {
            case SDK:
                if (individualClientInfo != null && individualClientInfo.isIndividualActive()) {
                    AppSubUserInfoDO individualUserInfoDO = appSubUserInfoDAO.getSubUserInfoByUid(individualClientInfo.getSubUid(), UserTypeEnum.UC_PERSON_TYPE);
                    if (individualUserInfoDO != null && SubUserStatusEnum.ACTIVE == individualUserInfoDO.getStatus()) {
                        resp.setSubUid(individualUserInfoDO.getSubUid());
                        resp.setUidType(UserTypeEnum.UC_PERSON_TYPE.getCode());
                    }
                }
                break;
            case APP:
            case H5:
            default:
                return setLastLoginUser(individualClientInfo, corpClientInfos);
        }
        return resp;
    }

    /**
     * 前端传了目标子用户登录
     *
     * @param reqDTO
     * @param allClientInfoResp
     */
    protected boolean setTargetSubUserFromParam(LoginRiskDTO reqDTO, AllClientInfoBO allClientInfoResp) {
        String targetEncryptedSubUid = reqDTO.getTargetEncryptedSubUid();
        UserTypeEnum userType = UserTypeEnum.getByCodeV2(reqDTO.getUserType());

        String targetSubUid = null;
        try {
            targetSubUid = authorizationCenterApi.decrypt(targetEncryptedSubUid);
        } catch (Exception e) {
            log.error(targetEncryptedSubUid + " decrypted error.", e);
            throw new BizException(BizErrorType.UID_DECRYPT_ERROR);
        }

        long subUid = Long.parseLong(targetSubUid);

        switch (userType) {
            case UC_PERSON_TYPE: {
                AppSubUserInfoDO appSubUserInfoDO = appSubUserInfoDAO.getSubUserInfoByUid(subUid, UserTypeEnum.UC_PERSON_TYPE);
                //当前子uid和shareUid不关联 则直接登录shareUid
                if (!reqDTO.getUid().equals(appSubUserInfoDO.getShareUid())) {
                    log.warn("target subUser`s sharUid not equals to shareUid in param.targetShareUid:{},pram shareUid:{}",
                            appSubUserInfoDO.getShareUid(), reqDTO.getUid());
                    return false;
                }
                //individual subUid 对应的retail cif是否为active
                if (!allClientInfoResp.isIndividualClientActive(subUid)) {
                    log.info("[login] individual client not inactive targetUid:{}", subUid);
                    return false;
                }
                break;
            }
            case UC_COMPANY_TYPE: {
                AppSubUserInfoDO appSubUserInfoDO = appSubUserInfoDAO.getSubUserInfoByUid(subUid, UserTypeEnum.UC_COMPANY_TYPE);
                //当前子uid和shareUid不关联 则直接登录shareUid
                if (!reqDTO.getUid().equals(appSubUserInfoDO.getShareUid())) {
                    log.warn("target subUser`s sharUid not equals to shareUid in param.targetShareUid:{},pram shareUid:{}",
                            appSubUserInfoDO.getShareUid(), reqDTO.getUid());
                    return false;
                }

                if (!allClientInfoResp.isCorporateClientActive(subUid)) {
                    log.info("[login] corporate client not inactive targetUid:{}", subUid);
                    return false;
                }

                break;
            }
            default: {
                throw BizErrorType.PARAM_CHECK_ERROR.wrap();
            }
        }

        reqDTO.setSubUid(subUid);
        reqDTO.setUidType(userType.getCode());
        return true;
    }

    /**
     * 设置上一次的登录子用户
     *
     * @param individualClientInfo
     * @param corpClientInfos
     */
    protected SubUserInfo setLastLoginUser(AllClientInfoBO.CommonClient individualClientInfo, List<? extends AllClientInfoBO.CommonClient> corpClientInfos) {
        SubUserInfo resp = new SubUserInfo();
        List<AppSubUserInfoDO> allActiveSubUser = Lists.newArrayList();
        AppSubUserInfoDO tmpIndividualUser = null;
        if (!CollectionUtils.isEmpty(corpClientInfos)) {
            Set<Long> corpUids = corpClientInfos
                    .stream()
                    .filter(AllClientInfoBO.CommonClient::isCorporateActive)
                    .map(AllClientInfoBO.CommonClient::getSubUid)
                    .collect(Collectors.toSet());
            allActiveSubUser.addAll(appSubUserInfoDAO.batchQueryCorpUserByCorpUids(corpUids));
        }
        if (individualClientInfo != null && individualClientInfo.isIndividualActive()) {
            tmpIndividualUser = appSubUserInfoDAO.getSubUserInfoByUid(individualClientInfo.getSubUid(), UserTypeEnum.UC_PERSON_TYPE);
            if (tmpIndividualUser != null && Objects.equals(SubUserStatusEnum.ACTIVE, tmpIndividualUser.getStatus())) {
                allActiveSubUser.add(tmpIndividualUser);
            }
        }
        AppSubUserInfoDO lastLoginSubUser = allActiveSubUser.stream().filter(item -> item.getStatus() == SubUserStatusEnum.ACTIVE)
                .max(Comparator.comparingLong(AppSubUserInfoDO::getLastLoginTime)).orElse(null);
        if (lastLoginSubUser == null) {
            log.error("not subUser or not lastLoginTime.subUsers:{}", LogMasker.toJSON(allActiveSubUser));
        } else if (lastLoginSubUser.getLastLoginTime() == 0L && tmpIndividualUser != null) {
            //subUser loginTime都为空时，优先个人户登录
            log.info("lastLoginSubUser`s loginTime is 0, Use individual user.lastLoginSubUser:{},tmpIndividualUser:{}", LogMasker.toJSON(lastLoginSubUser), LogMasker.toJSON(tmpIndividualUser));
            resp.setSubUid(tmpIndividualUser.getSubUid());
            resp.setUidType(tmpIndividualUser.getUserType().getCode());
        } else {
            log.info("lastLoginSubUser is : {}", LogMasker.toJSON(lastLoginSubUser));
            resp.setSubUid(lastLoginSubUser.getSubUid());
            resp.setUidType(lastLoginSubUser.getUserType().getCode());
        }
        return resp;
    }

    @Data
    public static class SubUserInfo {
        private Long subUid;
        private Integer uidType;
    }

}
