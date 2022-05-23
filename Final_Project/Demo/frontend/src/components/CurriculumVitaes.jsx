import React,{useState, useEffect} from "react";
import styled from "styled-components";
import CV from './CV';
import Logout from "./Logout";






const Container= styled.div`
    margin: 8px;
    border: 1px solid black;
    border-radius: 5px;
    width: 25%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-bottom: 10px;
    background-color: white;
`;

const BigContainer= styled.div`
    margin: 8px;
    border: 1px solid black;
    border-radius: 5px;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-bottom: 10px;
    background-color: white;
`;


function CurriculumVitaes(props){

    const initialData = {id:0, username:"", is_editor:false, is_active:true, email:"", CVs_ref:[]};
    const [user, setUser] = useState(initialData);

    const [showNewFieldButtom, setShowNewFieldButton]=useState(true);
    const [newCvName, setNewCvName]=useState('');
    const [deleted, setDeleted]=useState(false);

    const [changePassword, setchangePassword] = useState(false);

    /**
     * whenever showNewFieldButtom or deleted fire up generates a new token updates user
     */

    useEffect(() => {
        getNewToken();
        fetchCV().then(data=> setUser(data));
    }, [showNewFieldButtom,deleted]);

    /**
     * there we send a request to our api to gerate a new access token
     * and set global var in index.jx "token" to be that new access_token
     * memorizes it in a local storage
     */

    async function getNewToken(){
        const response = await fetch("auth/refresh",{
            method: "POST",
            headers: {
                "Authorization" : "Bearer " + props.refresh_token
            }
        });
        const data = await response.json();
        props.setToken(data.access_token);
        localStorage.setItem("access_token", JSON.stringify(data.access_token));
        
    }

      /**
     * there we fetch json about our user with his/ her CVs
     */


    async function fetchCV(){
      
        const response = await fetch("/users/CVs",{
            headers: {
                "Authorization" : "Bearer " + props.token
            }

        });
        const data = await response.json();
        return data;
                
            
        
        
    }

    /**
     * there we send request to create a new cv for the user
     */
    async function recordCv(){

        const to_pass = {user_id:user.id, name: newCvName};
        await fetch("users/create_cv",{
            method: "POST",
            headers: {
                "Authorization" : "Bearer " + props.token
            },
            body: JSON.stringify(to_pass)
        });
        setShowNewFieldButton(true);
    }

    /**
     * there we send request to delete a  cv for the user
     */
    async function deleteCv(id){
        setDeleted(true);
        const response = await fetch(`users/delete_cv/${id}`,{
            method: "DELETE",
            headers: {
                "Authorization" : "Bearer " + props.token
            },
        });
        setDeleted(false);

    }
    
     /**
     * there we send request to our api  to send a link for password changing on user email
     */
    async function sendEmail(){
        var emails = [];
        emails.push(user.email);
        const to_return = {
            email:emails,
            url: `http://localhost:3000/change_password?user_id=${user.id}`
        };
        await fetch(`users/email`,{
            method: "POST",
            headers: {
                "Content-type": "application/json"
              },
            body : JSON.stringify(to_return)
        });
        setchangePassword(true);
    }
    

    return(
        
        <div>
            
            {
                showNewFieldButtom? 
                <button onClick={() => setShowNewFieldButton(false)}>Create_a_cv</button>: 
                <div>
                    <input type="text" onChange={e => setNewCvName(e.target.value)}></input>
                    <button onClick={() => recordCv()}>Create</button>
                </div>
                
                
            }

            {
                changePassword? 
                <span>Follow the link that was just sent on your email</span>:
                <button onClick={sendEmail}>Change Password</button>
                
            }
         
            
            <Logout access_token={props.token} refresh_token={props.refresh_token}/>

            
            <BigContainer>
                {   
                    user.CVs_ref.map((ref, index) => {
                        return (<Container>
                                    <CV key={`cv_${ref.id}`}  name={ref.name} index={index} CVs_ref={ref} setUser = {setUser}/>
                                    <button  onClick={() => deleteCv(ref.id)}>delete</button>
                                </Container>
                        )
                    })
                }
            </BigContainer>
        </div>
        
        

        
    )
}
export default CurriculumVitaes