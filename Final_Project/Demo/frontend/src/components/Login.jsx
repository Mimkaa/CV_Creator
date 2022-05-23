import React,{useState} from "react";
import {useHistory, Link} from "react-router-dom";
import styled from "styled-components";
const Container = styled.div`
    display: flex;
    min-height: 100vh;
    flex-direction: column;
    justify-content: center;
    align-items: center;


`;

function Login(props){
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const history = useHistory();

     /**
     * 
     * calls  logineUser function and sets retrieved tokens in the local storage
     * 
     * 
     * 
     * 
     */
    function handleSubmit(e){
        e.preventDefault();
        
        loginUser().then(data => {
            localStorage.setItem("access_token", JSON.stringify(data.access_token));
            localStorage.setItem("refresh_token", JSON.stringify(data.refresh_token));
            props.setToken(data.access_token);
            props.setRefreshToken(data.refresh_token);
            history.push("/CurriculumVitaes");
        });

    }

     /**
     * 
     * calls  an api  to get access and refresh tokens
     * 
     * 
     * 
     * 
     */

    async function loginUser(){
        const formData = {
            username: username,
            password: password,
        };
        

        const response = await fetch("/auth/login",{
            
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData)
        });
        const data = await response.json();
        return data;
    }

    

    return (
        <Container>
            <form onSubmit={handleSubmit}>
                <p>
                    Username <input type='text' onChange={e => setUsername(e.target.value)}/>
                </p>
                <p>
                    Password <input type="password" onChange={e => setPassword(e.target.value)}/>
                </p>
                <p>
                    <button>Login</button>
                </p>
                <p>
                    <Link to = "/register">Need an accourt? Registe here</Link>
                </p>
            </form>
           
        </Container>
    )
}
export default Login