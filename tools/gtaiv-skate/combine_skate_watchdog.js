// Independent script: restore GTA if the main script stopped sending frames.
while (true) {
    wait(100);
    const {player,ped,camera}=native("COMBINE_SKATE_RESCUE");
    if (player<0) continue;
    const attempt=action=>{try{action();}catch(_){}};
    let recovered=true;
    const recover=action=>{try{action();}catch(_){recovered=false;}};
    recover(()=>native("ACTIVATE_SCRIPTED_CAMS",false,false));
    recover(()=>{if(native("DOES_CAM_EXIST",camera)) {
        native("SET_CAM_PROPAGATE",camera,false);native("SET_CAM_ACTIVE",camera,false);
        native("DESTROY_CAM",camera);
    }});
    recover(()=>{if(native("DOES_CHAR_EXIST",ped))native("FREEZE_CHAR_POSITION",ped,false);});
    recover(()=>native("SET_PLAYER_CONTROL",player,true));
    recover(()=>{if(!native("IS_PLAYER_CONTROL_ON",player)||native("DOES_CAM_EXIST",camera))throw new Error("recovery-unverified");});
    attempt(()=>native("COMBINE_SKATE_STOP"));
    if(recovered)attempt(()=>native("COMBINE_SKATE_RELEASE"));
}
