import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { EventEmitterService } from './../Services/event-emitter.service';
import { RestService } from './../Services/rest.service';

@Component({
  selector: 'app-personal-profile',
  templateUrl: './personal-profile.component.html',
  styleUrls: ['./personal-profile.component.css']
})
export class PersonalProfileComponent implements OnInit {

  constructor(
    private rs : RestService,
    private http : HttpClient, 
    private ees : EventEmitterService, 
    private router : Router,
    private route: ActivatedRoute) { }

  user : Account[] = [];
  username : string;
  usern : string;
  returnMsg: string;
  login = false;
  showpass = false;
  ngOnInit() {
    //only logged on user are allowed
    this.http.post('http://127.0.0.1:5000/getAccount',
    {token:localStorage.getItem('authToken')})
    .subscribe((response)=>{
      console.log(response['status']);
      if(response['status']!='success')
      {
        this.router.navigate(['/login']);
        this.ees.refreshName();
        alert("You are not logged in yet!")
      }
      else{
        this.login=true;
      }
    });

    this.http.post('http://127.0.0.1:5000/getAccount',
     {token:localStorage.getItem('authToken')})
    .subscribe((response)=>{
    console.log(response['status']);
    this.username=response['username'];
  });

  this.route.paramMap
    .subscribe(params => {
      this.usern = params.get('user');
      console.log(this.usern);
    })

  this.rs.readUserDataAll()
      .subscribe
        (
          (response) => 
          {
            this.user = response[0]["userdata"];
            console.log(this.user)
          },
          (error) =>
          {
            console.log("No Data Found" + error);
          }

        )
  }

  changePassword() {
    this.showpass = !this.showpass;
  }

  userChangePass(event) {
    event.preventDefault();
    const target = event.target;
    const oldpass = target.querySelector('#oldpassword').value;
    const pass1 = target.querySelector('#password1').value;
    const pass2 = target.querySelector('#password2').value;
    console.log(localStorage.getItem('authToken') + 'log')
    var info = {
      oldp: oldpass, p1: pass1, p2: pass2, token: localStorage.getItem('authToken'), user: this.usern
    };
    console.log(info);
    // this.us.getUserAndPass(username, password);
    this.http.post('http://127.0.0.1:5000/changepass', info)
        .subscribe((response)=>{
      this.returnMsg=response["msg"];
      console.log(this.returnMsg);
      // if(response["status"]=="success")
      // {
      //   localStorage.setItem('authToken', response["auth_token"]);
      //   console.log(localStorage.getItem('authToken'));
      //   this.router.navigate(['/']);
      //   this.ees.refreshName();
      // }
    });
  }
}
