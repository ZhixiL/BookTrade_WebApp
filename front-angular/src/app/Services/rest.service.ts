import { Injectable, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Textbook } from '../Textbook';
import { Account } from '../Account';

@Injectable({
  providedIn: 'root'
})
export class RestService implements OnInit {

  constructor(private http : HttpClient) { }

  ngOnInit(){
  }

  textbookUrl : string = "http://127.0.0.1:5000";
  userProfileUrl : string = "http://127.0.0.1:5000/profile"

  readTextbook()
  {
    return this.http.get<Textbook[]>(this.textbookUrl);
  }

  readUserData()
  {
    return this.http.get<Account[]>(this.userProfileUrl);
  }
}
