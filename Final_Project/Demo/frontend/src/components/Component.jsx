import React, {useState, useEffect} from "react";
import styled from "styled-components";
import Record from "./Record";
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

const ContainerRecord= styled.div`
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
const ContainerRecords= styled.div`
    margin: 8px;
    border: 1px solid black;
    border-radius: 5px;
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    padding-bottom: 10px;
    background-color: white;
`;

const Input = styled.div`
    display: flex;
`;

function Component(props){
    const [showNewFieldButtom, setShowNewFieldButton]=useState(true);
    

    const [variables, setVariables] = useState();
    

    useEffect(() => {
        createVariables().then(data=> setVariables(data))
    }, [showNewFieldButtom]);

     /**
     * 
     * we have passed which fields each component have from UnrolledCv
     * there we just convert this data to be an object like:
     * ["id","cv_id","name","extend"] => {"id":1,"cv_id":2,"name":"","extend":""}
     * 
     * 
     * 
     * 
     */
    async function createVariables(){

        const response = await fetch(`users/number_records/${props.head}`);
        const data = await response.json();

        let newFields ={cv_id:props.cv_id, id: data};

        props.fields.map((field) =>{
            newFields[field]='';
            
        });

        return newFields;
    }

    /**
     * 
     * we change fields by using this function in input elements
     * 
     * 
     * 
     * 
     */

    function doStuffWithVariables(val, field){
        
        if (field==="extend" && ! /^\d+$/.test(val)){
            setShowNewFieldButton(true);


        }else if (field==="extend" && /^\d+$/.test(val)){
            val = Number(val);
        };

        setVariables({
            ...variables,
            [field]: val
        })
    

    }

    /**
     * 
     * call to an api to delete a record
     * 
     * 
     * 
     * 
     */

    async function deleteFromDataBase(id){
        await fetch(`/users/delete_record/${props.head}/${id}`,{
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
        });
    }
    
    /**
     * 
     * it is used to delete the record from the current data about an antire cv
     * loaded on the page in frontend, then react will reloads the data in on the hooks
     * because data about a cv has been changed and a hook is set to keep track of such an event
     * 
     * 
     * 
     * 
     */

    function deleteRecord(id){
        deleteFromDataBase(id);
        var newElements = Array.from(props.cv_data[props.head])
        newElements = newElements.filter((item) => item.id !==id)
        props.setRefChange({
            ...props.cv_data,
            [props.head]: newElements
        });
    }

    /**
     * 
     * it is used to add a record to the current data about an antire cv
     * loaded on the page in frontend, then react will reloads the data in on the hooks
     * because data about a cv has been changed and a hook is set to keep track of such an event
     * 
     * 
     * 
     * 
     */
    
    function addRecord(){
        setShowNewFieldButton(true);
        let flag = false;
        Object.keys(variables).map((key, index) =>{
            if (variables[key] === "")
                flag = true;
            
        });
        if (flag){
            return;
        };
        var newElements = Array.from(props.cv_data[props.head])
        newElements.push(variables);

        props.setRefChange({
            ...props.cv_data,
            [props.head]: newElements

        });
    }

    
    return(
        <Container>
            <h3>{props.head}</h3>
                <ContainerRecords>
                   
                    {
                        
                        props.field_value.map((val,index) => {
                            return (<ContainerRecord key = {`container_${props.head}_${index}`}>
                                <button  onClick={() => deleteRecord(val.id)}>delete</button>

                               
                                <Record key = {`record_${props.head}_${index}`} data={val} cv_data = {props.cv_data} head = {props.head} index = {index} setRefChange = {props.setRefChange} />
                                </ContainerRecord>)
                                
                        })

                    }
                     
                </ContainerRecords>
                    
                <div>{
                    showNewFieldButtom?
                    <button onClick={() => setShowNewFieldButton(false)}>{`Add_to_${props.head}`}</button>:
                    <div>
                        {
                        props.fields.map((field,index)=>{
                            return <input key={`${props.head}_input_add_${index}`} type="text" placeholder={field} onChange={e => doStuffWithVariables(e.target.value,field)}></input>
                        })
                        
                    }
                    <button onClick={() => addRecord()}>Save</button>
                    </div>
                        
                    
                }
                </div>
                   
               
            
        </Container>
    )
}

export default Component;