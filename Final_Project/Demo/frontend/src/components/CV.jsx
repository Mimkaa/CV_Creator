import React,{useState, useEffect} from "react";
import styled from "styled-components";
import {useHistory, Link} from "react-router-dom";

const Container = styled.div`
    margin: 8px;
    border: 1px solid black;
    border-radius: 5px;
    width: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-bottom: 10px;
    background-color: white;
`;


function CV(props){
    return(
        <Container>
            <Link to = {{
                pathname:"/unfolded",
                search: `info=${JSON.stringify({ ...props.CVs_ref})}`
            }}>{props.name}</Link>
        </Container>
    )
}
export default CV;
