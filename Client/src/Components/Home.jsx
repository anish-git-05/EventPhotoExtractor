import {useState} from 'react'
import {API_URL} from '../api.js'
import '../Home.css'

function Home(){
    const [Folders, setFolders] = useState([])
    const [Loading, setLoading] = useState(false)

    const handleFileChange = (e) => {
        setFolders(e.target.files)
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        
        if(Folders.length === 0){
            alert("Please select at least one file")
            return
        }
        
        setLoading(true)
        
        const formData = new FormData();
        for (let i = 0; i < Folders.length; i++) {
            formData.append('images', Folders[i]);
        }

        try {
            const response = await fetch(`${API_URL}/process`, {
                method: 'POST',
                body: formData
            })

            if(response.ok){
                const blob = await response.blob();
                    
                const downloadUrl = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = downloadUrl;
                link.setAttribute('download', 'curated_album.zip');
                
                document.body.appendChild(link);
                link.click();
                
                link.parentNode.removeChild(link);
                window.URL.revokeObjectURL(downloadUrl);

                // --- THE NEW CLEANUP CODE ---
                
                // 1. Reset your React state (removes the "X photos ready" text)
                setFolders([]); 
                
                // 2. Reset the actual HTML form (clears the physical file input box)
                e.target.reset(); 
                
                // Optional: Let them know it's completely done
                alert("Success! Your curated album is downloading.");
                
                // ----------------------------

            } else {
                const data = await response.json()
                alert(data.error || "An error occurred on the server.")
            }
        } catch (err) {
            alert("Failed to connect to the server. Is Flask running?")
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