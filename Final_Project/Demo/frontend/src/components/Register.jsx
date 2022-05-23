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

function Register(props){
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const history = useHistory();

    /**
     * 
     * calls  createUser function and sets retrieved tokens in the local storage
     * 
     * 
     * 
     * 
     */
    function handleSubmit(e){
        e.preventDefault();
        
        createUser().then(data => {
            localStorage.setItem("access_token", JSON.stringify(data.access_token));
            localStorage.setItem("refresh_token", JSON.stringify(data.refresh_token));
            props.setToken(data.access_token);
            props.setRefreshToken(data.refresh_token);
            history.push("/CurriculumVitaes");
        });

    }

    /**
     * 
     * calls for an api to save a new user in the database
     * (uses some regex to prevent an invalid email input)
     * 
     * 
     * 
     * 
     */

    async function createUser(){
        const formData = {
            username: username,
            email: email,
            password: password,
        };
        if (! /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,})+$/.test(email)){
            document.getElementById("username").value='';
            document.getElementById("password").value='';
            document.getElementById("email").value='';
            setUsername("");
            setPassword("");
            setEmail("");
            return;
        };
        const response = await fetch("/auth/register",{
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
                    Username <input id="username" type='text' onChange={e => setUsername(e.target.value)}/>
                </p>
                <p>
                    Password <input id = 'password' type="password" onChange={e => setPassword(e.target.value)}/>
                </p>
                <p>
                    Email<input id = "email" type="text" onChange={e => setEmail(e.target.value)}/>
                </p>
                <p>
                    <button>Register</button>
                </p>
                <p>
                    <Link to = "/login">Already have an account? Login here</Link>
                </p>
            </form>
        </Container>
    )
}
export default Register