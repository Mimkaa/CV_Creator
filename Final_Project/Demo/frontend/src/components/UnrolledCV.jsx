import React , {useState, useEffect} from "react";
import xtype from "xtypejs"
import { useLocation} from "react-router-dom";
import styled from "styled-components";
import Component from "./Component";
import {useHistory, Link} from "react-router-dom";





const Title = styled.div`
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

const Container = styled.div`
    display: flex;
    min-height: 100vh;
    flex-direction: column;
    justify-content: center;
    align-items: center;


`;



function UnrolledCV(props){
       /**
     * 
     * first time the page is visited, the  data about it  is passed in query params
     * it is done to have something for default
     * 
     * 
     */
    const search = useLocation().search;
    const refString = new URLSearchParams(search).get("info");
    const ref  = JSON.parse(refString);
    const history = useHistory();

    const [refChange, setRefChange] = useState(ref);
    
    const initial = {"hobbies":[], "experiences":[], "contacts":[], "educations":[], "skills":[]};
    const [fields, setFields] = useState(initial);
    
    const [file, setFile] = useState(null);

  

        /**
     * 
     * there we fetch cv data with all details from api
     * 
     * 
     * 
     */
    async function fetchCVData(){
        const response = await fetch(`/users/get_cv/${ref.id}`)
        const data = await response.json();
        return data;
    }

       /**
     * 
     * when page is rendered, changes curent cv info by utilizing previous function
     * 
     * 
     * 
     * 
     */
    useEffect(() => {
        fetchCVData().then(data => setRefChange(data))
    }, []);

     /**
     * 
     * setting the fields variable to be a data about each cv detail fields
     * (is executed when page is rendered for the first time)
     * 
     * 
     * 
     * 
     */
   
    useEffect(() => {
        recordFields(refChange).then(data=> setFields(data))
    }, []);

      /**
     * 
     * whenever refChange i.e. loaded data about cv from api changes
     * we call first function below 
     * 
     * 
     * 
     * 
     */
    useEffect(()=>{
        saveRef();

    },[refChange])

   
       /**
     * 
     * there we send a request to the api to save all newly added components
     * 
     * 
     * 
     * 
     */
    async function saveRef(){
        const response = await fetch(`/users/save_cv/`,{
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(refChange)
        });
        history.replace(
        {
            pathname:"/unfolded",
            search: `info=${JSON.stringify({...refChange})}`,
            replace: true
        })
    }
 
    
      /**
     * 
     * this one is used to get which fileds each cv component have 
     * data looks like {skills:["id","cv_id","name","extend"]...}
     * 
     * 
     * 
     * 
     */

    async function recordFields(data){
        let fields = {};
        for (const [key , value] of Object.entries(data)){
            if (xtype.type(value)==="array"){
                
                const response = await fetch(`users/fields/${key}`);
                const data = await response.json();
                fields[key]= data;
            }
        }
        return fields;
    }

     /**
     * 
     * just sets file variable in the hook to be the first chosen file
     * 
     * 
     * 
     * 
     */
    function fileSelectHandler(e){
        setFile(e.target.files[0]);
    }

     /**
     * 
     * sends file to our api and reloads the page to see the result
     * 
     * 
     * 
     * 
     */

    async function fileUploadHandler() {
        let form_data = new FormData();
        form_data.append('file',file );
        await fetch(`/users/add_photo/${refChange.id}`,{
            
              method: 'POST',
              body: form_data
            });
        window.location.reload(false);
    }

     /**
     * 
     * image ration calculation
     * 
     * 
     * 
     * 
     */

    const onImageLoad = ({target:img}) =>{
        const {height, width} = img; 
        var ratio = (height/width);
        return ratio
    }

     /**
     * 
     * there we delete an uploaded image by requesting the api
     * and reload the file to see the results
     * 
     * 
     * 
     */

    async function deleteImage (){
        
        await fetch(`/users/delete_photo/${refChange.image.id}`,{
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
        });
        window.location.reload(false);
    }

    
    // a harder option of saving pdf implementation (had no courage to delete)
    // const exportPDF = () => {
    //     const input = document.getElementById("main")
    //     html2canvas(input,{logging: true, letterRendering: 1, useCORS: true, allowTaint:true}).then(canvas => {
    //         const imgWidth = 208;
    //         const imgHeight = canvas.height * imgWidth / canvas.width;
    //         const imgData = canvas.toDataURL("img/png");
    //         const pdf = new jsPDF("p", "mm", "a4");
    //         pdf.addImage(imgData, "PNG", 0,0, imgWidth, imgHeight);
    //         pdf.save(`${refChange.name}.pdf`);
    //     })
    // }

    

    return(
        <Container id = "main">
            <p>
                    <Link to = "/CurriculumVitaes">Back to Your CVs</Link>
            </p>
            <Title>
                <h1>{refChange.name}</h1> 
                <button onClick={window.print}>SAVE PDF</button>
            </Title>
            
            { 
            refChange.image?
                <div>
                    <p>
                        <span style= {{fontWeight: "bold"}} >Your_Image </span>: 
                    </p>    
                    <img  onLoad = {onImageLoad} src = {refChange.image.photo_url} width={100} height={onImageLoad*100}/>
                    <button onClick={() => deleteImage()}>Delete</button>
                </div>:
                <div>
                    <p>
                        <span style= {{fontWeight: "bold"}} >Your_Image </span>: 
                    </p>    
                    <input type="file" onChange = {fileSelectHandler}/>
                    <button onClick = {fileUploadHandler}>Upload</button>
                </div>
                
            }       
            
            {
                Object.entries(fields).map(([key,value],index) => (
                    <Component key={`${refChange.name}_${index}_${key}`} head = {key} fields = {value} field_value = {refChange[key]} cv_id = {refChange.id} cv_data = {refChange} setRefChange = {setRefChange}/>
                ))
               
            }
           
        </Container>
    )
}
export default UnrolledCV;
