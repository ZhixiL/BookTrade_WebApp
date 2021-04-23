import { Router } from '@angular/router';
import { EventEmitterService } from './../Services/event-emitter.service';
import { HttpClient, JsonpClientBackend } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Username, Textbook, Account } from './../model';
import { RestService } from './../Services/rest.service';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.css']
})

export class PostComponent implements OnInit {

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
  urllink:string = "assets/images/tempbook.jpg"
  ngOnInit()
  {
    //only logged on user are allow to use /post
    this.http.post('http://127.0.0.1:5000/getAccount',
    {token:localStorage.getItem('authToken')})
    .subscribe((response)=>{
      console.log(response['status']);
      if(response['status']!='success')
      {
        this.router.navigate(['/login']);
        this.ees.refreshName();
        alert("Please login before posting.")
      }
    });

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

  logForm(event) {
    event.preventDefault();
    const target = event.target;
    const bookname = target.querySelector('#BookName').value;
    const author = target.querySelector('#Author').value;
    const price = target.querySelector('#Price').value;
    const status = target.querySelector('#status').value;
    const college = target.querySelector('#college').value;
    const description = target.querySelector('#Description').value;
    console.log(localStorage.getItem('authToken') + 'log');

    const fd = new FormData();
      fd.append('file', this.selectedFile, this.selectedFile.name);

      this.http.post('http://127.0.0.1:5000/uploadFile', fd)
        .subscribe((response)=>
        {
          console.log(response);
          //this.urllink2 = <string>response["picUrl"];
        });

    var info = {
      token : localStorage.getItem('authToken'),
      pic: this.selectedFile.name,
      bookn: bookname,
      auth: author,
      pri: price, 
      stat: status,
      col: college,
      des: description
    };

    console.log(info);

    this.http.post('http://127.0.0.1:5000/post', info)
        .subscribe((response)=>
        { 
          this.returnMsg=response["msg"];
          console.log(this.returnMsg);

          if(response["status"]=="success")
          {
            localStorage.setItem('authToken', response["auth_token"]);
            console.log(localStorage.getItem('authToken'));
            this.router.navigate(['/']);
            this.ees.refreshName();
          }
        });

  }

  onFileSelected(event) {
    if(event.target.files){
      var reader = new FileReader()
      reader.readAsDataURL(event.target.files[0])
      reader.onload = (event:any)=>{
        this.urllink = event.target.result
      }
      this.selectedFile = <File>event.target.files[0];
    }
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
