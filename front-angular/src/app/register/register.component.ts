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

  constructor(
    private http : HttpClient, 
    private router: Router,
    private ees : EventEmitterService) { }

  user : AccountResgister[] = [];
  returnMsg: string;
  urllink:string = "assets/images/blank_profile.png"
  urllink2:string;
  selectedFile: File = null;

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
      event.preventDefault();
      const target = event.target;
      const firstname = target.querySelector('#firstName').value;
      const lastname = target.querySelector('#lastName').value;
      const username = target.querySelector('#username').value;
      const password1 = target.querySelector('#pwd1').value;
      const password2 = target.querySelector('#pwd2').value;
      const email = target.querySelector('#emailAddress').value;
      const fsuid = target.querySelector('#fsuId').value;
      console.log(localStorage.getItem('authToken') + 'log');

      if(firstname == "" || lastname == "" || username == "" ||
      password1 == "" || email == "" || fsuid == ""){
        alert("Please do not leave any field blank!");
        return 0; //terminate the process
      }

      if(password1!=password2){
        alert("The two passwords doesn't match!")
        return 0;
      }
      
      const fd = new FormData();
      fd.append('file', this.selectedFile, this.selectedFile.name);

      this.http.post('http://127.0.0.1:5000/uploadFile', fd)
        .subscribe((response)=>
        {
          console.log(response);
        });

      var info = {
        pic: this.selectedFile.name,
        firstn: firstname,
        lastn: lastname,
        usern: username, 
        pass1: password1,
        pass2: password2,
        emaila: email,
        fsu: fsuid
      };

      console.log(info);
      this.http.post('http://127.0.0.1:5000/createAccPage', info)
        .subscribe((response)=>
        { 
          this.returnMsg=response["msg"];
          console.log(this.returnMsg);

          if(response["status"]=="success")
          {
            localStorage.setItem('authToken', response["auth_token"]);
            console.log(localStorage.getItem('authToken'));
            this.router.navigate(['/']);
            this.ees.refreshName();
          }
        });
      
    }

    selectFiles(event){
      if(event.target.files){
        var reader = new FileReader()
        reader.readAsDataURL(event.target.files[0])
        reader.onload = (event:any)=>{
          this.urllink = event.target.result
        }
        this.selectedFile = <File>event.target.files[0];
      }
    }
  }