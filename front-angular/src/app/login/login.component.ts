import { Component, OnInit } from '@angular/core';
import { RestService } from '../Services/rest.service';
import { HttpClient, JsonpClientBackend } from '@angular/common/http';
import { Account, Username } from './../model';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  
  constructor(private rs : RestService, private us: RestService, private http : HttpClient) {}

  headers = [ "username", "password"]
  user : Account[] = [];
  returnMsg: string;
  
  ngOnInit() {
    
    this.rs.readAccData()
    .subscribe
    (
      (response) =>
      {
          this.user = response[0]["data"];
      },
      (error) =>
      {
          console.log("No Data Found" + error)
      }
    )
  }

  userLogin(event) {
    event.preventDefault();
    const target = event.target;
    const username = target.querySelector('#username').value;
    const password = target.querySelector('#password').value;
    var info = {
      usern: username, pass: password
    };
    console.log(info);
    // this.us.getUserAndPass(username, password);
    this.http.post('http://127.0.0.1:5000/login', info)
        .subscribe((response)=>{
      this.returnMsg=response["msg"];
      console.log(this.returnMsg);
    });
  }
  
} 
