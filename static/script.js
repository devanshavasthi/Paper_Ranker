var home=document.getElementById("homeDiv");
var about=document.getElementById("aboutDiv");
var education=document.getElementById("educationDiv");
var publication=document.getElementById("publicationDiv");
var help=document.getElementById("helpDiv");
var content=document.getElementById("content");
var time= document.getElementById("demo");
var t= new Date();
basics();
function basics() {
    content.innerHTML = home.innerHTML;
}
function fhome() {
    content.innerHTML = home.innerHTML;
    document.body.style.backgroundImage = "linear-gradient(rgba(0,0,0,0.5),rgba(0,0,0,0.5)),url('https://drive.google.com/uc?export=view&id=1AwecV-U4LSb2ADbE5dS8ml7eFjCjwTo5')";

}
function fabout() {
    content.innerHTML = about.innerHTML;
    document.body.style.backgroundImage = "linear-gradient(rgba(0,0,0,0.5),rgba(0,0,0,0.5)),url('https://drive.google.com/uc?export=view&id=1AwecV-U4LSb2ADbE5dS8ml7eFjCjwTo5')";
    
}
function feducation() {
    content.innerHTML = education.innerHTML;
    document.body.style.backgroundImage = "linear-gradient(rgba(0,0,0,0.5),rgba(0,0,0,0.5)),url('https://drive.google.com/uc?export=view&id=1AwecV-U4LSb2ADbE5dS8ml7eFjCjwTo5')";
}
function display_c(){
    var refresh=1000; // Refresh rate in milli seconds
    mytime=setTimeout('timing()',refresh)
}
function timing() {
    var x = new Date()
    var x1=x.toUTCString();
    document.getElementById('demo').innerHTML = x1;
    display_c();
}
timing();
