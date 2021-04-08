import { Component, OnInit } from '@angular/core';
import { Textbook, Account } from './../model';
import { RestService } from '../Services/rest.service';
import { HttpClient, JsonpClientBackend } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';
@Component({
  selector: 'app-book-detail',
  templateUrl: './book-detail.component.html',
  styleUrls: ['./book-detail.component.css']
})
export class BookDetailComponent implements OnInit {

  constructor(
    private rs : RestService,
    private route: ActivatedRoute,
    private router:Router,
    private http: HttpClient,
    ) { }
  textbook : Textbook[] = [];
  tbook : string;
  currentUsername : string;

  ngOnInit()
  {
    this.rs.readTextbookAll()
      .subscribe
        (
          (response2) => 
          {
            this.textbook = response2[0]["bookdata"];
          },
          (error) =>
          {
            console.log("No Data Found" + error);
          }
        )
    this.http.post('http://127.0.0.1:5000/getAccount',
      {token:localStorage.getItem('authToken')})
        .subscribe((response)=>{
          console.log(response['status']);
          if(response['status']=='success')
          {
            this.currentUsername = response['usern']
          }else{
            this.currentUsername = "offline"
          }
    });

    this.route.paramMap
        .subscribe(params => {
          this.tbook = params.get('bookname');
          console.log(this.tbook);
        })
  }

  changePrice(id) {
    const np = document.getElementById("priceUpdate");
    var newPrice = Number(np.innerHTML)
    if(Number.isNaN(newPrice)){
      alert("Please enter number or decimal number only!")
    }else{
      this.http.post('http://127.0.0.1:5000/priceChange',
      {token:localStorage.getItem('authToken'),
      id:id,
      newP:newPrice})
        .subscribe((response)=>{
          alert(response['msg'])
        })
    }
  }

  deletePost(id) {
    this.http.post('http://127.0.0.1:5000/deletePost',
    {token:localStorage.getItem('authToken'),id:id})
      .subscribe((response)=>{
        alert(response['msg'])
        this.router.navigate(['/'])
      })
  }

  editDes(id) {
    const nd = document.getElementById("desUpdate");
    var newDes = String(nd.innerHTML)
    this.http.post('http://127.0.0.1:5000/descriptionChange',
    {token:localStorage.getItem('authToken'),
    id:id,
    newD:newDes})
      .subscribe((response)=>{
        alert(response['msg'])
      })
  }

}
