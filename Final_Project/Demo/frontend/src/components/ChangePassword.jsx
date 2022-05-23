import React,{useState} from "react";
import {useHistory, Link, useLocation, Redirect } from "react-router-dom";
import styled from "styled-components";
const Container = styled.div`
    display: flex;
    min-height: 100vh;
    flex-direction: column;
    justify-content: center;
    align-items: center;


`;

function ChangePassword(props){
    const search = useLocation().search;
    const refString = new URLSearchParams(search).get("user_id");
    const user_id  = Number(refString);
    const [NewPassword, setNewPassword] = useState('');
    const [ConfirmNewPassword, ConfirmsetNewPassword] = useState('');
    const history = useHistory();
    
    

     /**
     * 
     * calls  an api to update a user and redirects to "/login"
     * 
     * 
     * 
     * 
     */
    
    async function changePassword(e){
        history.push("/login");
        if (NewPassword!==ConfirmNewPassword || NewPassword===""){
            document.getElementById("newpassword").value='';
            document.getElementById("confirmnewpassword").value='';
            return;
        };

        await fetch(`/users/change_password/${user_id}`,{
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({new_password:NewPassword})
        });
        

    }

    return (
        <Container>
            <form onSubmit={changePassword}>
                <p>
                    NewPassword<input id ="newpassword" type="text" onChange={e => setNewPassword(e.target.value)}/>
                </p>
                <p>
                    ConfirmNewPassword<input id ="confirmnewpassword" type="text" onChange={e => ConfirmsetNewPassword(e.target.value)}/>
                </p>
                <p>
                    <button>Confirm</button>
                </p>
                <p>
                    <Link to = "/login">to Login</Link>
                </p>
            </form>
        </Container>
    )
}
export default ChangePassword