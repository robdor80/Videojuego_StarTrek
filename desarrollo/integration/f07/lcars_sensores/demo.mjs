/* Synthetic operator-visible demo only. No F06 host truth, canon, or real scan. */
export const DEMO={
  schema:"f07.observer.v1",
  session:{ship_label:"USS SUTHERLAND",station_label:"SENSORES",tick:28800,
    revision:1,source:"DEMO",sensors_online:true},
  capabilities:{track:true,focus:true,science:false},
  contacts:[
    {id:"C-001",status:"active",position_milli_au:[980,-420,0],
      distance_milli_au:1066,confidence_permille:680,observed_category:1,
      class_id:0,class_label:null,transponder_id:null,last_seen:28800,
      tracking_mode:0,model:null},
    {id:"C-002",status:"active",position_milli_au:[1000,390,0],
      distance_milli_au:1073,confidence_permille:810,observed_category:1,
      class_id:0,class_label:null,transponder_id:null,last_seen:28780,
      tracking_mode:0,model:null},
    {id:"C-003",status:"active",position_milli_au:[-490,-260,0],
      distance_milli_au:554,confidence_permille:960,observed_category:13,
      class_id:0,class_label:null,transponder_id:null,last_seen:28795,
      tracking_mode:0,model:null},
    {id:"C-004",status:"active",position_milli_au:[-750,570,0],
      distance_milli_au:942,confidence_permille:520,observed_category:11,
      class_id:0,class_label:null,transponder_id:null,last_seen:28770,
      tracking_mode:0,model:null},
    {id:"C-005",status:"active",position_milli_au:[270,-780,0],
      distance_milli_au:825,confidence_permille:890,observed_category:14,
      class_id:0,class_label:null,transponder_id:null,last_seen:28795,
      tracking_mode:0,model:null}
  ],
  notices:[
    {id:"N-001",kind:"new",tick:28400,contact_id:"C-001"},
    {id:"N-002",kind:"new",tick:28500,contact_id:"C-003"},
    {id:"N-003",kind:"new",tick:28780,contact_id:"C-005"}
  ],
  results:[]
};
