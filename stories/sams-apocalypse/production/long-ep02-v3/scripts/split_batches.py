from pathlib import Path
import json,wave,time,hashlib
import numpy as np
P=Path(__file__).resolve().parents[1];D=P/'audio/batches';batches=json.loads((D/'batch-plan.json').read_text())
while True:
    pending=[]
    for b in batches:
        meta=D/(b['id']+'.json');wav=D/(b['id']+'.wav')
        if not meta.exists() or not wav.exists():pending.append(b['id']);continue
        m=json.loads(meta.read_text())
        if not m.get('alignment'):pending.append(b['id']);continue
        rows=m['alignment']
        if isinstance(rows,dict):rows=rows.get('subtitles') or rows.get('sentences') or rows.get('data')
        assert isinstance(rows,list) and rows
        words=[word for row in rows for word in row.get('timestamped_words',[])];assert words,b['id']
        assert ''.join(c['tts_text'] for c in b['cues'])==m['request']['text']
        with wave.open(str(wav)) as w:
            params=w.getparams();sr=w.getframerate();pcm=w.readframes(w.getnframes());samples=np.frombuffer(pcm,dtype='<i2');n=len(samples)
        assert params.nchannels==1 and params.sampwidth==2
        boundaries=[0];boundary_proof=[]
        for c in b['cues'][:-1]:
            char=c['text_end'];prev=[w for w in words if w['word_end']<=char];nxt=[w for w in words if w['word_begin']>=char];assert prev and nxt,(b['id'],c['id'])
            assert not any(w['word_begin']<char<w['word_end'] for w in words),'Boundary through a provider word'
            a=max(w['time_end'] for w in prev)/1000;z=min(w['time_begin'] for w in nxt)/1000
            assert z>=a-.08,(a,z)
            point=round((a+z)/2*sr);assert boundaries[-1]<point<n
            # Select the lowest 5ms energy spot within a 20ms guard around the exact word boundary.
            lo=max(boundaries[-1]+1,point-round(.020*sr));hi=min(n-1,point+round(.020*sr));window=max(1,round(.005*sr))
            choices=range(lo,hi+1,max(1,round(.001*sr)))
            point=min(choices,key=lambda x:float(np.mean(samples[max(0,x-window//2):min(n,x+window//2)].astype(np.float32)**2)))
            boundaries.append(point);boundary_proof.append({'after_cue':c['id'],'char_boundary':char,'previous_word_time_end':a,'next_word_time_begin':z,'selected_audio_time':point/sr})
        boundaries.append(n)
        for c,a,z in zip(b['cues'],boundaries,boundaries[1:]):
            out=P/'audio/raw'/(c['id']+'.wav');outmeta=out.with_suffix('.metadata.json')
            if out.exists() and outmeta.exists():continue
            assert not out.exists() and not outmeta.exists(),'Partial output requires review'
            with wave.open(str(out),'wb') as w:w.setparams(params);w.writeframes(pcm[a*2:z*2])
            cm={'provider':'MiniMax','endpoint':'https://api.minimax.cn/v1/t2a_v2','http_status':m['http_status'],'base_status_code':m['base_status_code'],'trace_id':m['trace_id'],'preset':m['preset'],'request':m['request'],'request_text_scope':'entire_parent_batch','parent_batch':b['id'],'batch_text_begin':c['text_begin'],'batch_text_end':c['text_end'],'source_cue_text':c['tts_text'],'batch_audio_start_sample':a,'batch_audio_end_sample':z,'batch_audio_sample_rate':sr,'word_boundary_proof':boundary_proof,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'subtitle_files_generated':False,'alignment_usage':'Provider JSON used internally for sentence slicing; no independent SRT/VTT created'}
            outmeta.write_text(json.dumps(cm,ensure_ascii=False,indent=2)+'\n');print(f"Aligned {c['id']} from {b['id']}",flush=True)
    if not pending:break
    time.sleep(2)
print('All generated batches split to original speech cues',flush=True)
