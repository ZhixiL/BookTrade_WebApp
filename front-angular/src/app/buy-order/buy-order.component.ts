import { Router } from '@angular/router';
import { EventEmitterService } from './../Services/event-emitter.service';
import { HttpClient, JsonpClientBackend } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Username, Textbook, Account } from './../model';
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
    private rs : RestService,
    private ees : EventEmitterService,
    private router : Router
    ) { }

  textbooks : Textbook[] = [];
  constTXBK : Textbook[] = [];
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

    this.rs.readTextbookAll()
    .subscribe
      (
        (responses) => 
        {
          this.constTXBK = this.textbooks = responses[0]["bookdata"];
        },
        (error) =>
        {
          console.log("No Data Found" + error);
        }
      )
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

  onFileSelected(event) {
    this.selectedFile = event.target.files[0];
  }

  onUpload() {
    const fd = new FormData();
    fd.append('image', this.selectedFile)
    this.http.post('http://127.0.0.1:5000/buyorder', fd, {
      reportProgress: true,
      observe: 'events'      
    })
      .subscribe(event => {
        console.log(event);
      });
  }

  postService (event: any) {
    this.textbooks = this.constTXBK; 
  }
  
}
