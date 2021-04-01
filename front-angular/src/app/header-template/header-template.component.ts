import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { EventEmitterService } from './../Services/event-emitter.service';
import { RestService } from './../Services/rest.service';
import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-header-template',
  templateUrl: './header-template.component.html',
  styleUrls: ['./header-template.component.css']
})
export class HeaderTemplateComponent implements OnInit {

  constructor(
    private ees : EventEmitterService,
    private http : HttpClient,
    private router : Router
    ) {}
  username : string;
  usern : string;

  ngOnInit()
  {
    this.http.post('http://127.0.0.1:5000/getAccount',
     {token:localStorage.getItem('authToken')})
    .subscribe((response)=>{
    console.log(response['status']);
    this.username=response['username'];
    this.usern = response['usern'];
  });

    if (this.ees.refreshSubVar==undefined) {    
      this.ees.refreshSubVar = this.ees.
      invokeHeaderRefresh.subscribe((name:string) => {    
        this.refreshUser();
      }); 
    }
  }

  refreshUser()
  {
    this.http.post('http://127.0.0.1:5000/getAccount',
     {token:localStorage.getItem('authToken')})
    .subscribe((response)=>{
    console.log(response['status']);
    this.username=response['username'];
    this.usern = response['usern'];
  });
  }
  listSearch(event)
  {
    const target = event.target;
    const key = target.querySelector('#key').value;
    this.router.navigate(['/booklist']);
    setTimeout(() => 
    {
      this.ees.searchButtonClick(key);
    }, //avoid function conflict
    200);
  }
  
}
