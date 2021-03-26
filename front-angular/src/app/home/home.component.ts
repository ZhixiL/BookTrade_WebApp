import { EventEmitterService } from './../Services/event-emitter.service';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { Textbook } from './../model';
import { Component, OnInit } from '@angular/core';
import { RestService } from '../Services/rest.service';
import { escapeRegExp } from '@angular/compiler/src/util';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(
    private rs : RestService,
    private http : HttpClient,
    private ees : EventEmitterService
    ){}

  headers = ["author", "bookname", "by", "college", "description",
              "id", "picture", "price", "stat", "time"]

  textbook : Textbook[] = [];
  login = false;
  ngOnInit()
  {
    //verify if user has logged on or not.
    this.refreshLoginMenu()
    this.rs.readTextbook()
    .subscribe
      (
        (response) => 
        {
          this.textbook = response[0]["bookdata"];
        },
        (error) =>
        {
          console.log("No Data Found" + error);
        }

      )
  }
  refreshLoginMenu()
  {
    this.http.post('http://127.0.0.1:5000/getAccount',
    {token:localStorage.getItem('authToken')})
    .subscribe((response)=>{
      console.log(response['status']);
      if(response['status']=='success')
      {
        this.login=true;
      }else{
        this.login=false;
      }
    });
  }
  logout()
  {
    this.http.post('http://127.0.0.1:5000/signout',
    {token:localStorage.getItem('authToken')})
    .subscribe((response)=>{
      alert(response['msg']);
      this.ees.refreshName();
      this.refreshLoginMenu();
    });
  }

}
