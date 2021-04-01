import { EventEmitterService } from './../Services/event-emitter.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';
import { RestService } from '../Services/rest.service';
import { HttpClient, JsonpClientBackend } from '@angular/common/http';
import { Account } from './../model';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  
  constructor(
    private rs : RestService, 
    private router : Router,
    private http : HttpClient,
    private ees : EventEmitterService,
    ) {}

  headers = [ "username", "password"]
  user : Account[] = [];
  returnMsg: string;

  ngOnInit() {
  //verify if user has logged on or not.
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
    const keeplogin = target.querySelector('#keeplogin').checked;
    console.log(localStorage.getItem('authToken') + 'log')
    var info = {
      usern: username, pass: password,
      token: localStorage.getItem('authToken'),
      keeplog: keeplogin
    };
    console.log(info);
    // this.us.getUserAndPass(username, password);
    this.http.post('http://127.0.0.1:5000/login', info)
        .subscribe((response)=>{
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
  
} 
