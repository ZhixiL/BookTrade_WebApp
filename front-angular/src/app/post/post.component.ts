import { HttpClient, JsonpClientBackend } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Username, Textbook, Account } from './../model';
import { RestService } from './../Services/rest.service';
import {NgForm} from '@angular/forms';
import { flushMicrotasks } from '@angular/core/testing';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.css']
})

export class PostComponent implements OnInit {

  selectedFile: File = null;
  constructor(private http : HttpClient, private rs : RestService) { }

  textbooks : Textbook[] = [];
  constTXBK : Textbook[] = [];
  accounts : Account[] = [];
  returnMsg : string;
  ngOnInit()
  {
    this.rs.readTextbookAll()
    .subscribe
      (
        (response) => 
        {
          this.constTXBK = this.textbooks = response[0]["bookdata"];
                  
        },
        (error) =>
        {
          console.log("No Data Found" + error);
        }
      )
  }

  logForm(value) {
    console.log(value);
    this.http.post('http://127.0.0.1:5000/post', value)
        .subscribe((response)=>{
      this.returnMsg=response["response"];
      console.log(this.returnMsg);
    });
  }

  onFileSelected(event) {
    this.selectedFile = event.target.files[0];
  }
  onUpload() {
    const fd = new FormData();
    fd.append('image', this.selectedFile)
    this.http.post('http://127.0.0.1:5000/post', fd, {
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
