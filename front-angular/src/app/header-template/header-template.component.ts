import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { EventEmitterService } from './../Services/event-emitter.service';
import { RestService } from './../Services/rest.service';
import { Component, OnInit } from '@angular/core';
import { Textbook, Account, Textbooks } from './../model';

@Component({
  selector: 'app-header-template',
  templateUrl: './header-template.component.html',
  styleUrls: ['./header-template.component.css']
})
export class HeaderTemplateComponent implements OnInit {

  constructor(
    private rs : RestService,
    private ees : EventEmitterService,
    private http : HttpClient,
    private router : Router
    ) {}
  username : string;
  usern : string;
  profilepic : string;
  accountInfo : Account[];
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

    this.rs.readUserDataAll()
    .subscribe
    (
      (response) =>
      {
          this.profilepic = "../../assets/images/profilepic.png";
          this.accountInfo = response[0]["userdata"];
          for (var u of this.accountInfo)
          {
            if (u.avatar != "profilepic.png" && u.username == this.usern)
            {
              console.log("test in if")
              this.profilepic = "../../assets/images/" + u.avatar;
            }
          }
          console.log(this.profilepic)
      },
      (error) =>
      {
          console.log("No Data Found" + error)
      }
    )
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
