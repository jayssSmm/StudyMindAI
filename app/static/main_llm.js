
const statusEle=document.getElementById('status')
const aiForm=document.getElementById('ai-form')
const submitBtn=document.getElementById('submit')

const newSessBtn = document.getElementById('new-session-btn')
const sidebar = document.getElementById('history-sidebar');
const overlay = document.getElementById('sidebar-overlay');

const sessList = document.getElementById('sessions-list')

function getGuestId() {
    const existing = localStorage.getItem("guest_id")
    if (existing) return existing          // reuse across refreshes

    const newId = crypto.randomUUID()
    localStorage.setItem("guest_id", newId)
    return newId
}

const guestId = getGuestId()

let session_id = null

document.addEventListener('DOMContentLoaded', () => {
    newSessBtn.addEventListener('click',()=>{
        session_id = null
        statusEle.textContent='Waiting for your prompt...'
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');

        document.getElementById('input').focus();
    })

    sessList.addEventListener('click', (e)=>{
        const item = e.target.closest('.session-item');

        if (item) {
            session_id = item.dataset.id; // Now this will not be undefined
            statusEle.textContent='Waiting for your prompt...'

            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
            document.getElementById('input').focus();
        }
    })
})