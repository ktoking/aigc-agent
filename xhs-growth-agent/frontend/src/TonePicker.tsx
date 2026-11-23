export const TONES = [
  {id:'natural',label:'自然',description:'像日常聊天，直接说具体的事'},
  {id:'critical',label:'批判',description:'指出具体问题和不合理处'},
  {id:'objective',label:'客观',description:'事实、观点和未知分开，克制表达'},
  {id:'subjective',label:'主观',description:'从个人看法、偏好和感受出发'},
  {id:'sharp',label:'犀利',description:'抓核心，观点直接，句子有力'},
  {id:'gentle',label:'温和',description:'措辞平和，不训人、不拱火'},
  {id:'humorous',label:'幽默',description:'轻松吐槽，少量贴切比喻'},
  {id:'empathetic',label:'共情',description:'看见普通人的具体处境和感受'},
] as const;
export type Tone = typeof TONES[number]['id'];
export const toneNames = (values?: string[]) => (values?.length ? values : ['natural']).map(id => TONES.find(t => t.id === id)?.label ?? id).join('＋');

export function TonePicker({value,onChange,disabled=false}: {value:Tone[];onChange:(value:Tone[])=>void;disabled?:boolean}) {
  return <fieldset className="tone-picker" disabled={disabled}>
    <legend>表达语气 <span>可组合，最多 4 个</span></legend>
    <div className="tone-tags">{TONES.map(tone => <button type="button" key={tone.id} aria-pressed={value.includes(tone.id)} title={tone.description} disabled={disabled || value.length >= 4 && !value.includes(tone.id)} onClick={() => onChange(value.includes(tone.id) ? value.filter(id => id !== tone.id) : [...value,tone.id])}>{tone.label}</button>)}</div>
    <p>本次：{toneNames(value)}。始终自然表达，少套话，不固定批判。</p>
  </fieldset>;
}
