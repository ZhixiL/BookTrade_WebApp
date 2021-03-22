import { Component, OnInit } from '@angular/core';
import { RestService } from '../Services/rest.service';
import { HttpClient, JsonpClientBackend } from '@angular/common/http';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  /**
  constructor(private rs : RestService) {}

  headers = ["username", "password"]

  user : Account[] = [];
  */
  ngOnInit(): void {
    /**
    this.rs.readInputData()
    .subscribe
    (
      (response) =>
      {

      },
      (error) =>
      {

      }
    )*/
  }
  
} 
