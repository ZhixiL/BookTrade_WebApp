import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
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
    private http : HttpClient, 
    private ees : EventEmitterService, 
    private router : Router) { }
  username : string;
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
    });

    this.http.post('http://127.0.0.1:5000/getAccount',
     {token:localStorage.getItem('authToken')})
    .subscribe((response)=>{
    console.log(response['status']);
    this.username=response['username'];
  });
  }

}
