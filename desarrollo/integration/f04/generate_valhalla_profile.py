"""Compile the approved 90-row document into immutable profile data. No people stored here."""
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / 'proyecto/docs/roadmap/master/fases/F04/F04-VALHALLA-01_PLANTILLA_1800_Y_CIVILES_400.md'

def rows():
    text = SOURCE.read_text(encoding='utf-8').split('## Cuadrante de referencia sección por sección')[1].split('## Civilización')[0]
    result = []
    for dept, block in zip([3, 2, 1, 5, 6, 7, 4], text.split('### ')[1:]):
        for line in block.splitlines():
            cells = [c.strip() for c in line.strip('|').split('|')]
            if len(cells) == 6 and all(re.fullmatch(r'\d+', c) for c in cells[1:]):
                result.append((len(result)+1, dept, cells[0], *map(int, cells[1:])))
    assert len(result) == 90
    assert [sum(r[i] for r in result) for i in range(3, 8)] == [1800, 550, 380, 255, 615]
    assert all(r[3] == sum(r[4:]) for r in result)
    return result

def render():
    data = rows()
    # Explicit operational qualifications. Dedicated auxiliary and Marine skills
    # never alias Valhalla command/helm/engineering/tactical authorization.
    skills = {
      3: (3,1), 4:(8,2), 5:(9,1), 6:(9,1), 7:(32,1), 8:(9,1), 9:(9,1), 10:(9,1),11:(9,1),12:(36,0),
      13:(2,8),14:(10,8),15:(10,8),16:(11,8),17:(11,8),18:(13,8),19:(13,8),20:(12,8),21:(13,8),22:(13,8),23:(13,8),24:(13,8),25:(13,8),26:(37,0),
      27:(1,4),28:(1,4),29:(15,1024),30:(16,1024),31:(17,1024),32:(33,1024),33:(18,1024),34:(18,1024),35:(14,1024),36:(18,1024),37:(15,1024),38:(18,1024),
      39:(5,64),40:(19,16),41:(20,32),42:(5,64),43:(21,64),44:(5,64),45:(5,64),46:(5,64),47:(34,16),48:(21,64),49:(21,64),50:(5,64),51:(38,0),
      52:(6,128|4096),53:(22,128),54:(22,128),55:(22,128),56:(23,4096),57:(23,4096),58:(23,4096),59:(24,4096),60:(22,128),61:(24,4096),62:(39,0),
      63:(41,0),64:(42,0),65:(42,0),66:(42,0),67:(42,0),68:(43,0),69:(44,0),70:(45,0),
      71:(7,256|2048),72:(25,256),73:(26,256),74:(26,256),75:(26,256),76:(27,2048),77:(27,2048),78:(27,2048),79:(26,256),80:(26,256),
      81:(4,512),82:(28,512),83:(29,512),84:(35,512),85:(30,512),86:(28,512),87:(31,512),88:(28,512),89:(28,512),90:(40,0)}
    skills.update({1:(3,1),2:(3,1)})
    lines = ['#pragma once', '// Generated from the approved document; regenerate with generate_valhalla_profile.py.',
      'inline constexpr F04TemplateSpec valhalla{F04_VALHALLA_FLAGSHIP,1800,400,8191,"valhalla","valhalla_flagship_2387","exploration_defense_civil_community","author_approved_target_2387"};',
      'inline constexpr std::array<F04SectionSpec,90> valhalla_sections{{']
    for s,d,name,total,a,b,g,o in data:
        q,station = skills[s]
        area = 'Defiant acoplada' if s in [12,26,51,62,90] else 'Destacamento Hijos de Odín' if 63<=s<=70 else 'Platillo: hangar principal' if s==73 else 'Sección motriz: hangares auxiliares' if s==74 else 'Sección motriz: warp y puente de batalla' if s in [14,16,17,23] else 'Valhalla: servicios comunes; adscripción de separación pendiente'
        lines.append(f' {{{s},{d},{total},{a},{q},{station},2,"{name}","{name}; competencia propia sin mando naval implícito","{area}"}},')
    lines += ['}};', 'inline constexpr std::array<F04WatchDemand,90> valhalla_demands{{']
    lines += [f' {{{s},{a},{b},{g},{o}}},' for s,d,name,total,a,b,g,o in data]
    lines += ['}};', '''inline uint64_t valhalla_group(uint64_t s) {
 if(s==12 || s==26 || s==51 || s==62 || s==90)return F04_DEFIANT_NAVAL;
 if(s>=63 && s<=70)return F04_ODIN_MARINE;
 return F04_VALHALLA_NAVAL;
}
inline uint64_t valhalla_responsibility(uint64_t s,uint64_t o) {
 if(s==1)return F04_CAPTAIN;
 if(s==2)return F04_FIRST;
 if(s==81 && o==1)return F04_DOCTOR;
 if((s==13 || s==27 || s==39 || s==52 || s==71) && o<=2)return o==1?F04_HEAD:F04_DEPUTY;
 return 0;
}
inline uint64_t valhalla_qualifications(const F04SectionSpec& s) {
 uint64_t m=1ULL<<s.qualification;
 if(s.id==28)m|=1ULL<<F04_Q_ASTROMETRY;
 if(s.id==52)m|=1ULL<<F04_Q_TACTICAL;
 if(s.id==81 || s.id==84)m|=1ULL<<F04_Q_CLINICAL;
 return m;
}
inline constexpr uint64_t valhalla_continuous[]={F04_ST_COMMAND,F04_ST_HELM,F04_ST_SENSORS,F04_ST_COMPUTER,F04_ST_COMMUNICATIONS,F04_ST_ENGINEERING,F04_ST_TACTICAL,F04_ST_MEDICAL};''']
    return '\n'.join(lines)+'\n'

if __name__ == '__main__':
    (HERE/'src/f04_valhalla.h').write_text(render(), encoding='utf-8')
    (HERE/'tests/fixtures/valhalla_approved.tsv').write_text(''.join('\t'.join(map(str,(s,total,a,b,g,o)))+'\n' for s,d,name,total,a,b,g,o in rows()), encoding='utf-8')
