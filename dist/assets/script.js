fetch("companies.json")
.then(r=>r.json())
.then(data=>{
  window.companies=data;
  render(data);
})
.catch(()=>document.getElementById("list").innerHTML="Failed to load companies.json");

function render(data){
  let html="";
  data.forEach(c=>{
    html+=`
    <div class="card">
      <h3>${c.name}</h3>
      <p><b>${c.location}</b></p>
      <p>${c.description}</p>
      <a class="whatsapp" href="https://wa.me/255716002790">WhatsApp</a>
    </div>`;
  });
  document.getElementById("list").innerHTML=html;
}

function search(){
  let q=document.getElementById("search").value.toLowerCase();
  let f=window.companies.filter(c=>JSON.stringify(c).toLowerCase().includes(q));
  render(f);
}
