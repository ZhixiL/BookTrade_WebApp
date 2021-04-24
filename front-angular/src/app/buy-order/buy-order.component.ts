import { Router } from '@angular/router';
import { EventEmitterService } from './../Services/event-emitter.service';
import { HttpClient, HttpEventType, JsonpClientBackend } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Account } from './../model';
import { RestService } from './../Services/rest.service';

@Component({
  selector: 'app-buyorder',
  templateUrl: './buy-order.component.html',
  styleUrls: ['./buy-order.component.css']
})

export class BuyOrderComponent implements OnInit {

  selectedFile: File = null;
  constructor(
    private http : HttpClient, 
    private ees : EventEmitterService,
    private router : Router
    ) { }

  accounts : Account[] = [];
  returnMsg : string;
  ngOnInit()
  {
    //only logged on user are allow to use /post
    this.http.post('http://127.0.0.1:5000/getAccount',
    {token:localStorage.getItem('authToken')})
    .subscribe((responses)=>{
      console.log(responses['status']);
      if(responses['status']!='success')
      {
        this.router.navigate(['/login']);
        this.ees.refreshName();
        alert("Please login before posting.")
      }
    });

  }

  logForm(value) {
    var data = {
      token : localStorage.getItem('authToken'),
      bookdata : value,
    }
    this.http.post('http://127.0.0.1:5000/buyorder', data)
        .subscribe((responses)=>{
      this.returnMsg=responses["responses"];
      console.log(this.returnMsg);
      alert(this.returnMsg);
      this.router.navigate(['/buyorder'])
    });
  }

  
}
