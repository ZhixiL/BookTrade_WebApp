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
  
  constructor(private rs : RestService) {}

  headers = [ "username", "password"]
  user : Account[] = [];
  
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
  
} 
