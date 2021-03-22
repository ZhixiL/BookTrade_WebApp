import { HttpClient, JsonpClientBackend } from '@angular/common/http';
import { RestService } from './../Services/rest.service';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  
  //Every Account needs to have a unique username, email, and fsuid
  firstname:string;
  lastname:string;
  username:string;
  password1:string;
  password2:string;
  email:string;
  fsuid:string;

  constructor(private http : HttpClient, private router: Router) { }
  
  ngOnInit(): void {
  }

  onClickSubmit(data){
    this.firstname = data.firstname;
    this.lastname = data.lastname;
    this.username = data.username;
    this.password1 = data.password1;
    this.password2 = data.password2;
    this.email = data.email;
    this.fsuid = data.fsuid;
    
    let result1 = this.validateData();

    if(result1 == true){
      let Account = {
        firstName: this.firstname,
        lastName: this.lastname,
        user: this.username,
        pwd: this.password1,
        mail: this.email,
        FSUid: this.fsuid
      }

      this.http.post('http://127.0.0.1:5000/createAccPage', JSON.stringify(Account))
        .subscribe(
          (response)=>
          { 
            //result will contain either some type of error or it will contain
            //the string "sucessful"
            let result = response;
            if( result == "sucessful" ){
              console.log("NewAccount: " + result);
              this.router.navigate(['/login']);
            }
            else {
              console.log("NewAccount: " + result);
              alert(result);
            }
          }  
          )
    }
  }
  
  //checks to make sure that valid data has been entered
  //checks the to make sure the size of data entered is appropriate
  //check to make sure that password1 and password2 are the same
  validateData(){
    if(this.firstname.length > 30 || this.lastname.length == 0){
      alert("FirstName must be between 1 and 30 characters long");
      return false;
    }
    if(this.lastname.length > 30 || this.lastname.length == 0){
      alert("LastName must be between 1 and 30 characters long");
      return false;
    }
    if(this.username.length > 30 || this.username.length == 0){
      alert("Username must be between 1 and 30 characters long");
      return false;
    }
    if(this.password1.length > 15 || this.password1.length == 0){
      alert("Password must be between 1 and 15 characters long");
      return false;
    }
    if(this.password1 != this.password2){
      alert("Password and confirm password do not match");
      return false;
    }
    if(this.email.length > 100 || this.email.length == 0){
      alert("Email must be between 1 and 100 characters long");
      return false;
    }
    if(this.fsuid.length > 10 || this.fsuid.length == 0){
      alert("Fsuid must be between 1 and 10 characters long");
      return false;
    }
    console.log("New Account: UserInput has correct length and passwords match");
    return true;
  }
  
}
