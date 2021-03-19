import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  // constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  // login(): string {
  //     this.http.get('http://127.0.0.1:5000/ping')
  //   return "pong";
  // }
}
