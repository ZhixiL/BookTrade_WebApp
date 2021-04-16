import { AccountResgister } from './../model';
import { HttpClient, JsonpClientBackend } from '@angular/common/http';
import { RestService } from './../Services/rest.service';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { EventEmitterService } from './../Services/event-emitter.service';
@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  
  //Every Account needs to have a unique username, email, and fsuid
  // firstname:string;
  // lastname:string;
  // username:string;
  // password1:string;
  // password2:string;
  // email:string;
  // fsuid:string;

  constructor(
    private http : HttpClient, 
    private router: Router,
    private ees : EventEmitterService) { }

  user : AccountResgister[] = [];
  returnMsg: string;
  urllink:string = "assets/images/blank_profile.png"

  ngOnInit(){
    this.http.post('http://127.0.0.1:5000/getAccount',
    {token:localStorage.getItem('authToken')})
    .subscribe((response)=>{
    console.log(response['status']);
    if(response['status']=='success')
    {
      this.router.navigate(['/']);
      this.ees.refreshName();
      alert("You've already logged on!")
    }
  });
  }

  onClickSubmit(event){
      alert("test")
      // event.preventDefault();
      // const target = event.target;
      // const firstname = target.querySelector('#firstName').value;
      // const lastname = target.querySelector('#lastName').value;
      // const username = target.querySelector('#username').value;
      // const password1 = target.querySelector('#pwd1').value;
      // const password2 = target.querySelector('#pwd2').value;
      // const email = target.querySelector('#emailAddress').value;
      // const fsuid = target.querySelector('#fsuId').value;
      // console.log(localStorage.getItem('authToken') + 'log')
      // var info = {
      //   firstn: firstname,
      //   lastn: lastname,
      //   usern: username, 
      //   pass1: password1,
      //   pass2: password2,
      //   emaila: email,
      //   fsu: fsuid
      // };
      // console.log(info);
      // this.http.post('http://127.0.0.1:5000/createAccPage', info)
      //   .subscribe((response)=>
      //     { 
      //       this.returnMsg=response["msg"];
      //       console.log(this.returnMsg);

      //       if(response["status"]=="success")
      //       {
      //         localStorage.setItem('authToken', response["auth_token"]);
      //         console.log(localStorage.getItem('authToken'));
      //         this.router.navigate(['/']);
      //         this.ees.refreshName();
      //       }
      //     });
    }

    selectFiles(event){
      if(event.target.files){
        var reader = new FileReader()
        reader.readAsDataURL(event.target.files[0])
        reader.onload = (event:any)=>{
          this.urllink = event.target.result
        }
      }
    }
  }
  
  /*

  const imgDiv= document.querySelector('profile-pic-div');
  const img = <HTMLElement>document.querySelector('#photo');
  const file = document.querySelector('#file');
  const uploadBtn = <HTMLElement>document.querySelector('#uploadBtn');

  
  //if user hovers over profile div
  imgDiv.addEventListener('mouseenter', function()
  {
    uploadBtn.style.display="block";
    //document.getElementById("uploadBtn").style.display="block";
  });

  //if we hover out from img div 
  imgDiv.addEventListener('mouseleave', function()
  {
    uploadBtn.style.display="none";
    //document.getElementById("uploadBtn").style.display="none";
  });
  
  //lets work for image showing functionality when we shoose an 
  //image to upload

  
  //when we choose a photo to upload
  file.addEventListener('change', function(){
    //this referes to file
    const choosedFile = this.files[0];

    if(choosedFile){
      //FileReader is a predefined function of JS
      const reader = new FileReader(); 
    
      reader.addEventListener('load', function(){
        img.setAttribute('src', reader.result as string);
      });

      reader.readAsDataURL(choosedFile);
    }
  });
  */
  //checks to make sure that valid data has been entered
  //checks the to make sure the size of data entered is appropriate
  //check to make sure that password1 and password2 are the same
  // validateData(){
  //   if(this.firstname.length > 30 || this.lastname.length == 0){
  //     alert("FirstName must be between 1 and 30 characters long");
  //     return false;
  //   }
  //   if(this.lastname.length > 30 || this.lastname.length == 0){
  //     alert("LastName must be between 1 and 30 characters long");
  //     return false;
  //   }
  //   if(this.username.length > 30 || this.username.length == 0){
  //     alert("Username must be between 1 and 30 characters long");
  //     return false;
  //   }
  //   if(this.password1.length > 15 || this.password1.length == 0){
  //     alert("Password must be between 1 and 15 characters long");
  //     return false;
  //   }
  //   if(this.password1 != this.password2){
  //     alert("Password and confirm password do not match");
  //     return false;
  //   }
  //   if(this.email.length > 100 || this.email.length == 0){
  //     alert("Email must be between 1 and 100 characters long");
  //     return false;
  //   }
  //   if(this.fsuid.length > 10 || this.fsuid.length == 0){
  //     alert("Fsuid must be between 1 and 10 characters long");
  //     return false;
  //   }
  //   console.log("New Account: UserInput has correct length and passwords match");
  //   return true;
  // }
  
// }
