import {useState,useRef} from 'react'
import {API_URL} from '../api.js'
import '../Home.css'
import imageCompression from 'browser-image-compression';

function Home(){
    const inputRef=useRef(null);
    const [topk,settopk]=useState('');
    const [Folders, setFolders] = useState([]);
    const [Loading, setLoading] = useState(false);
    const [Feedback,setFeedback]=useState({});
    const [LoadFeedback,setLoadFeedback]=useState(false);
    const handleFileChange = (e) => {
        setFolders(e.target.files);
    }
    const handletopkInputChange=(e)=>{
        settopk(e.target.value);
    }
    const handleSubmit = async (e) => {
        e.preventDefault()
        const options={
            maxSizeMB:0.5,
            maxWidthOrHeight:1920,
            useWebWorker:true
        }
        if(Folders.length === 0){
            alert("Please select at least one file")
            return
        }
        setLoading(true)
        try{
            let response;
            const formData=new FormData();
            let flag=1;
            const chunkSize=5;
            for (let i =0;i<Folders.length;i++) {
                const compressedFile=await imageCompression(Folders[i],options);
                formData.append('images',compressedFile,Folders[i].name);
                if(((i+1)%chunkSize==0 && i>0)||i==Folders.length-1){
                    response = await fetch(`${API_URL}/upload/files`, {
                        method: 'POST',
                        body: formData
                    })
                    if(!response.ok){
                        const data = await response.json()
                        alert(data.error || "An error occurred on the server.")
                        flag=0;
                        break;
                    }
                    formData.delete('images');
                }
            }
            response=await fetch(`${API_URL}/upload/topk`,{
                method:"POST",
                headers:{
                    'content-type':'application/json'
                },
                body:JSON.stringify({'topk':topk})
            });
            const data=await response.json();
            if(response.ok){
                console.log("topk value uploaded successfully!")
            }else{
                console.log(data.error||"topk value not uploaded");
            }
            if(!flag){
                alert("Upload failed. Please try again.");
                return;
            }
            response=await fetch(`${API_URL}/process`);
            if(response.ok){
                const blob=await response.blob();
                const downloadURL=window.URL.createObjectURL(blob);
                const link=document.createElement('a');
                link.href=downloadURL;
                link.setAttribute('download','curated_album.zip');
                document.body.appendChild(link);
                link.click();
                link.parentNode.removeChild(link);
                window.URL.revokeObjectURL(downloadURL);
                setFolders([]); 
                document.getElementById('file-upload').value=''; 
                if(inputRef.current){
                    inputRef.current.value="";
                }
                alert("Success! Your curated album is downloaded.");
            }else{
                const data=await response.json();
                alert(data.error|| "Processing failed. Please try again.");
            }
        } catch (err) {
            alert("Failed to connect to the server. Please try again later.")
            console.error(err);
        } finally {
            setLoading(false);
            setLoadFeedback(true);
        }
    }
    const handleInputChange=(e)=>{
            const {name,value}=e.target;
            setFeedback((prevFeedback)=>({
                ...prevFeedback,[name]:value
            }));
        };
    const handleFeedback=async (e)=>{
        e.preventDefault();
        const response=await fetch(`${API_URL}/feedback`,{
            method:'POST',
            headers:{
                'content-type':'application/json'
            },
            body:JSON.stringify(Feedback)
        });
        const data=await response.json();
        if(response.ok){
            alert("Feedback Submitted!");
            console.log(data,"Feedback submitted succesfully!");
        }else{
            alert("Feedback submission error. Please try again");
            console.log(data.error||"Error in feedback submission");
        }
        setLoadFeedback(false);
    };

    return(
        <div className='home'>
            <div className='intro'>
                <h1>Event Photo Extraction</h1>
                <h2>Extract the best photos captured in your event!</h2>
            </div>
            <div className='filepath'>
                <form onSubmit={handleSubmit}>
                    
                    <label htmlFor='file-upload'>
                        Select Event Photos:
                    </label>

                    <input 
                        type='file' 
                        id='file-upload' 
                        multiple 
                        ref={inputRef}
                        accept='image/*' 
                        onChange={handleFileChange}
                    />

                    {Folders.length > 0 && (
                        <p>
                            {Folders.length} photos ready for upload!
                        </p>
                    )}
                    <p>Choose how many of the best photos you want. If not chosen, by default atmost 8 photos will be chosen.</p>
                    <input name="topk" type="number" min='1' max={Folders.length} onChange={handletopkInputChange} className='topkinput'></input>
                    <button disabled={Loading} type='submit'>
                        {Loading ? "Processing..." : "Extract Best Photos"}
                    </button>
                </form>
            </div>
            {LoadFeedback&&
                <div className='feedback'>
                    <form className='feedbackForm' onSubmit={handleFeedback}>
                            <p>How do you rate the average quality selection of your photos?</p>
                            <p>Very poor=1 and Very good=5</p>
                            <input type='number' name='quality' min='1' max='5' placeholder='1-5' onChange={handleInputChange}></input>
                            <p>On a scale of 1-5 how unique are the photos?</p>
                            <input type='number' name='uniqueness' min='1' max='5' placeholder='1-5' onChange={handleInputChange}></input>
                            <button type='submit'>Submit feedback</button>
                    </form>
                </div>
            }   
            <div>
                <h3>How to use:</h3>
                <p>I: Click the "Select Event Photos" button and choose the event photos.</p>
                <p>II: Click the "Extract Best Photos" button to start the extraction process.</p>
            </div>
            <p>Note: The curated zip folder will be saved in your downloads folder</p>
        </div>
    )
}

export default Home