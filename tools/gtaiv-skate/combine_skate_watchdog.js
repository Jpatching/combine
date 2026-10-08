// Independent script: restore GTA if the main script stopped sending frames.
while (true) {
    wait(100);
    const {player,ped,camera}=native("COMBINE_SKATE_RESCUE");
    if (player<0) continue;
    const attempt=action=>{try{action();}catch(_){}};
    attempt(()=>native("ACTIVATE_SCRIPTED_CAMS",false,false));
    attempt(()=>{if(native("DOES_CAM_EXIST",camera)) {
        native("SET_CAM_PROPAGATE",camera,false);native("SET_CAM_ACTIVE",camera,false);
        native("DESTROY_CAM",camera);
    }});
    attempt(()=>{if(native("DOES_CHAR_EXIST",ped))native("FREEZE_CHAR_POSITION",ped,false);});
    attempt(()=>native("SET_PLAYER_CONTROL",player,true));
    native("COMBINE_SKATE_STOP");native("COMBINE_SKATE_RELEASE");
}
