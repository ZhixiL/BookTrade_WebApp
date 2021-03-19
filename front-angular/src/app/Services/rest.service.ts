import { Injectable, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Textbook } from '../Textbook';

@Injectable({
  providedIn: 'root'
})
export class RestService implements OnInit {

  constructor(private http : HttpClient) { }

  ngOnInit(){
  }

  textbookUrl : string = "http://127.0.0.1:5000";

  readTextbook()
  {
    return this.http.get<Textbook[]>(this.textbookUrl);
  }
}
