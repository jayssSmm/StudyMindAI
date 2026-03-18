const statusEle=document.getElementById('status')
const aiForm=document.getElementById('ai-form')
const submitBtn=document.getElementById('submit')

aiForm.addEventListener('submit',()=>{
    statusEle.textContent='Thinking..'
    submitBtn.disabled=true
})

window.addEventListener('pageshow',()=>{
    submitBtn.disabled=false
})


const dropZone=document.getElementById('drop-zone')
const dropBox=document.getElementById('drop-box')

dropZone.addEventListener('dragover', (e)=>{
    e.preventDefault()
})

dropZone.addEventListener('drop', (e)=>{
    e.preventDefault()
    const dropData=e.dataTransfer.files
    dataHandler(dropData)
})

dropZone.addEventListener('click', (e)=>{
    dropBox.click()
})

dropBox.addEventListener('change', (e)=>{
    dataHandler(e.target.files)
})

dropBox.addEventListener('paste', (e)=>{
    const pasteData=e.clipboardData.files
    dataHandler(pasteData)
})

function dataHandler(files){

    const maxSize=10*1024*1024

    for (let i=0;i<files.length;i++){
        let currentFile=files[i]
        if (currentFile.size>maxSize){
            alert('File size Exceeds 10MB limit')
            return
        }else{
            uploadFile(files[i])
        }
    }
}

function uploadFile(file){
    const formData = new FormData()

    formData.append("file", file)

    fetch("/upload", {
    method: "POST",
    body: formData
    })
    .then (response=>response.json())
    .then (data=>statusEle.textContent=(data.message))
}
