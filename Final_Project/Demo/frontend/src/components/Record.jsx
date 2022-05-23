import React , {useState, useEffect}from "react";
import styled from "styled-components";

const Name = styled.h1`
    padding: 5px;
`;

const Container = styled.div`

    
    padding: 5px;
`;






function Record(props){

    const [showNewFieldButtom1, setShowNewFieldButton1]=useState(true);
    const [variablesEdit, setVariablesEdit] = useState();
    
    /**
     * 
     * sends a request to api to change data in database
     * and then changes data of entire cv, retrieve a new data of
     * the entire cv
     * 
     * 
     * 
     * 
     */

    async function editRecord(){
        setShowNewFieldButton1(true);
        const response = await fetch(`users/edit/comp/${props.head}/${variablesEdit.id}`,{
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(variablesEdit),
        });

        let flag = false;
        Object.keys(variablesEdit).map((key, index) =>{
            if (variablesEdit[key] === "")
                flag = true;
            
        });
        if (flag){
            return;
        };

        var newElements = Array.from(props.cv_data[props.head])
        const Updated = newElements.map((obj,index) =>{
            return obj.id === variablesEdit.id ? variablesEdit:obj;
        })

        props.setRefChange({
            ...props.cv_data,
            [props.head]: Updated

        });
        
    }

    /**
     * 
     * when the button is clicked changes in to input fields in "render"
     * 
     * 
     * 
     * 
     */


    function ChangeToEditing(val){
        setVariablesEdit(val);
        setShowNewFieldButton1(false)
    }
    
    /**
     * 
     * we change fields by using this function in input elements
     * 
     * 
     * 
     * 
     */


    function doStuffWithVariablesEdit(val, field){
        
        if (field==="extend" && ! /^\d+$/.test(val)){
            setShowNewFieldButton1(true);


        }else if (field==="extend" && /^\d+$/.test(val)){
            val = Number(val);
        };

        setVariablesEdit({
            ...variablesEdit,
            [field]: val
        })
    

    }

    


    return (
            
            <div>
                
                {
                    Object.keys(props.data).map((key, index) =>{

                    if (!key.includes("id")){
                        return <Container  key = {`repr_${key}_${index}`}><span style= {{fontWeight: "bold"}}>{key}</span>:  {props.data[key]}</Container>;};

                    })}
                
                {
                showNewFieldButtom1?
                    <button onClick={() => ChangeToEditing(props.data)}>edit</button>:
                    <div>
                        {
                        Object.keys(props.data).map((key, index) =>{
                            if (!key.includes("id")){
                                return <input key = {`input_${key}_${index}`} type="text" defaultValue={props.data[key]} onChange={e => doStuffWithVariablesEdit(e.target.value,key)}></input>
                            };
                        })
                        
                    }
                    <button onClick={() => editRecord()}>Save</button>
                    </div>
                }

            </div>
            
            
      
        
       
    )
}



export default Record;