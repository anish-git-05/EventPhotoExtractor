import {useState} from 'react'
import {API_URL} from '../api.js'
import '../Home.css'
import imageCompression from 'browser-image-compression';

function Home(){
    const [Folders, setFolders] = useState([])
    const [Loading, setLoading] = useState(false)

    const handleFileChange = (e) => {
        setFolders(e.target.files)
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
                    response = await fetch(`${API_URL}/upload`, {
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
                alert("Success! Your curated album is downloaded.");
            }else{
                const data=await response.json();
                alert(data.error|| "Processing failed. Please try again.");
            }
                
                // ----------------------------
        } catch (err) {
            alert("Failed to connect to the server. Please try again later.")
            console.error(err)
        } finally {
            setLoading(false)
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
                    
                    <label htmlFor='file-upload'>
                        Select Event Photos:
                    </label>

                    <input 
                        type='file' 
                        id='file-upload' 
                        multiple 
                        accept='image/*' 
                        onChange={handleFileChange}
                    />

                    {Folders.length > 0 && (
                        <p>
                            📎 {Folders.length} photos ready for upload.
                        </p>
                    )}
                    
                    <button disabled={Loading} type='submit'>
                        {Loading ? "Processing..." : "Extract Best Photos"}
                    </button>
                </form>
            </div>
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