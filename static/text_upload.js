import { marked } from 'https://cdn.jsdelivr.net/npm/marked/+esm'

const statusEle=document.getElementById('status')
const aiForm=document.getElementById('ai-form')
const submitBtn=document.getElementById('submit')

submitBtn.addEventListener('click',()=>{
    statusEle.textContent='Thinking..'
    submitBtn.disabled=true

    const prompt=document.getElementById('input').value
    const model=document.getElementsByName('name').value
    fetch('/',{
        method:'POST',
          headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'prompt': prompt,
            'model': model
        })
    })
    .then(data=>statusEle.innerHTML=marked.parse(data))
})

window.addEventListener('pageshow',()=>{
    submitBtn.disabled=false
})