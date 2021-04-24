import { Username, Textbook, Textbooks, Account } from './../model';
import { Injectable, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class RestService implements OnInit {
  
  
  constructor(private http : HttpClient) { }

  ngOnInit(){
  }
  baseUrl : string = "http://127.0.0.1:5000";
  readTextbook()
  {
    return this.http.get<Textbook[]>(this.baseUrl + "/booklistbrief");
  }

  readTextbookProfile()
  {
    return this.http.get<Textbook[]>(this.baseUrl + "/profilebook");
  }

  readTextbookAll()
  {
    return this.http.get<Textbook[]>(this.baseUrl + "/booklistall");
  }

  readBuyOrderAll()
  {
    return this.http.get<Textbooks[]>(this.baseUrl + "/buylist");
  }
  readUserData()
  {
    return this.http.get<Account[]>(this.baseUrl + "/profile");
  }

  readUserDataAll()
  {
    return this.http.get<Account[]>(this.baseUrl + "/userdataall");
  }

  readUsernameData()
  {
    return this.http.get<Username[]>(this.baseUrl + "/usernamedata");
  }

  readAccData() 
  {
    return this.http.get<Account[]>(this.baseUrl + "/login");
  }
}
