import React from "react";
import {Link, useHistory} from "react-router-dom";

function Logout(props){
    const history = useHistory();

    async function revokeAccess(){
        const response = await fetch("auth/logout_access",{
            method: "POST",
            headers: {
                "Authorization" : "Bearer " + props.access_token
            }
        });
    }
    async function revokeRefresh(){
        const response = await fetch("auth/logout_refresh",{
            method: "POST",
            headers: {
                "Authorization" : "Bearer " + props.refresh_token
            }
        });
    }
    

    function logoutUser(){
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        revokeAccess();
        revokeRefresh();
        history.push("/login");

    }
    return(
        <button onClick={logoutUser}>logout</button>
    )
}
export default Logout;