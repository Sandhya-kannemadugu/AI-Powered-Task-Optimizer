
const ctx=document.getElementById('chart');

new Chart(ctx,{
type:'line',
data:{
labels:["1","2","3","4","5","6"],
datasets:[{
label:"Emotion Level",
data:[2,3,4,3,5,4],
borderWidth:3
}]
}
});
