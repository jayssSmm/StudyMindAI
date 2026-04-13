import { marked } from 'https://cdn.jsdelivr.net/npm/marked/+esm'

const statusEle=document.getElementById('status')
const aiForm=document.getElementById('ai-form')
const submitBtn=document.getElementById('submit')

aiForm.addEventListener('submit',(e)=>{

    e.preventDefault()

    statusEle.textContent='Thinking..'
    submitBtn.disabled=true

    const prompt=document.getElementById('input').value
    const model=document.getElementById('model').value

    document.getElementById('input').value=''

    fetch('/prompt',{
        method:'POST',
        credentials:'include',
        headers: {
            'Content-Type': 'application/json',
            "x-guest-id": guestId,
        },
        body: JSON.stringify({
            'prompt': prompt,
            'model': model,
            'session_id': session_id,
        })
    })
    .then (response=>response.json())
    .then (data=>{
        console.log("Response body:", data)
        statusEle.innerHTML = marked.parse(data.message)
        session_id = data.session_id
    })
    .finally(()=>{
        submitBtn.disabled=false
    })
})