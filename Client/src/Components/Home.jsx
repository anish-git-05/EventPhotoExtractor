import {useState} from 'react'
import {API_URL} from '../api.js'
import '../Home.css'
function Home(){
    const [Folders, setFolders] = useState({})
    const [Loading, setLoading] = useState(false)
    const handleSubmit=async (e)=>{
        e.preventDefault()
        setLoading(true)
        const response= await fetch(`${API_URL}/process`,{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                inputFolder:e.target.path.value,
                outputFolder:e.target.output.value
            })
        })
        const data=await response.json()
        setLoading(false)
        if(response.ok){
            setFolders(data)
        }else{
            alert(data.error)
        }
    }
    return(
        <div className='home'>
            <div className='intro'>
                <h1>Event Photo Extraction</h1>
                <h2>Extract the best photos captured in your event!</h2>
            </div>
            <div className='filepath'>
                <form onSubmit={handleSubmit}>
                    <label htmlFor='path'>Input Folder:</label>
                    <input type='text' id='path' name='path' required placeholder='Enter the path to the folder containing event photos'/>
                    <label htmlFor='output'>Output Folder:</label>
                    <input type='text' id='output' name='output'placeholder='Enter the path to the folder where you want to save the best photos'/>
                    <button disabled={Loading} type='submit'>{Loading?"Processing...":"Extract Best Photos"}</button>
                </form>
                <p style={{marginTop:'20px'}}>Note:If you don't enter the output folder or if the output folder doesn't exist, a folder with the name of Input folder +"_curated" will be created in the same parent folder as of the input folder</p>
            </div>
        </div>
    )
}

export default Home
