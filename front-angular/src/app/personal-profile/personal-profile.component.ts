import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { EventEmitterService } from './../Services/event-emitter.service';
import { RestService } from './../Services/rest.service';
import { Textbook, Account, Textbooks } from './../model';
@Component({
  selector: 'app-personal-profile',
  templateUrl: './personal-profile.component.html',
  styleUrls: ['./personal-profile.component.css']
})
export class PersonalProfileComponent implements OnInit {

  constructor(
    private rs : RestService,
    private rs2 : RestService,
    private http : HttpClient, 
    private ees : EventEmitterService, 
    private router : Router,
    private route: ActivatedRoute) { }

  user : Account[] = [];
  buyorders : Textbooks[] = [];
  buyorders2 : Textbooks[] = [];
  textbook : Textbook[] = [];
  textbook2 : Textbook[] = [];
  constTXBK : Textbook[] = []; //permanently hold textbooks for the session, in case if textbooks is manipulated.
  username : string;
  usern : string;
  returnMsg: string;
  login = false;
  showpass = false;
  showbooklist = true;
  showbuyorder = false;
  initial : number = 0;
  final : number = 8;
  pageNums;
  initial2 : number = 0;
  final2 : number = 4;
  pageNums2;
  bookpic: string;
  defaultpic:string = "default_book.jpg";
  defaultpiclink:string = "../../assets/images/default_book.jpg";
  booklink:string = "../../assets/images/";
  ngOnInit() {
    //only logged on user are allowed
    this.http.post('http://127.0.0.1:5000/getAccount',
    {token:localStorage.getItem('authToken')})
    .subscribe((response)=>{
      console.log(response['status']);
      if(response['status']!='success')
      {
        this.router.navigate(['/login']);
        this.ees.refreshName();
        alert("You are not logged in yet!")
      }
      else{
        this.login=true;
        if(response['pic'] == "none"){
          this.profilepic = "../../assets/images/profilepic.png"
        }else{
          this.profilepic = "../../assets/images/" + response['pic']
        }
      }
    });

    this.http.post('http://127.0.0.1:5000/getAccount',
     {token:localStorage.getItem('authToken')})
    .subscribe((response)=>{
    console.log(response['status']);
    this.username=response['username'];
  });

  this.route.paramMap
    .subscribe(params => {
      this.usern = params.get('user');
      console.log(this.usern);
    })

  this.rs.readUserDataAll()
    .subscribe
      (
        (response) => 
        {
          this.user = response[0]["userdata"];

        },
        (error) =>
        {
          console.log("No Data Found" + error);
        }

      )

  this.rs.readTextbookAll()
  .subscribe
    (
      (response2) => 
      {
        this.textbook = response2[0]["bookdata"];
        this.bookpic = "../../assets/images/profilepic.png";
      for (var tb of this.textbook)
      {
        if (tb.by==this.usern)
        {
          (this.textbook2).push(tb);
          console.log(tb);
        }
      }
      this.pageNums = Array(Math.ceil(this.textbook2.length/8)).fill(0).map((x,i)=>i);

      },
      (error) =>
      {
        console.log("No Data Found" + error);
      }
    )

  this.rs2.readBuyOrderAll()
  .subscribe
    (
      (response3) => 
      {
        this.buyorders = response3[0]["bookdatas"];
      for (var tb of this.buyorders)
      {
        if (tb.by==this.usern)
        {
          (this.buyorders2).push(tb);
          console.log(tb);
        }
      }
      this.pageNums2 = Array(Math.ceil(this.buyorders2.length/4)).fill(0).map((x,i)=>i);
      },
      (error) =>
      {
        console.log("No Data Found" + error);
      }
    )
  }


  pageChange(pgNum)
  {
    this.initial = pgNum*8;
    this.final = (pgNum+1)*8;
  }

  pageChangeBuy(pgNum)
  {
    this.initial2 = pgNum*4;
    this.final2 = (pgNum+1)*4;
  }

  changePassword() {
    this.showpass = !this.showpass;
  }

  postedBooks() {
    this.showbooklist = !this.showbooklist;
    this.showbuyorder = !this.showbuyorder;
  }

  deleteBuyOrder(bkid) {
    var info = {
      bkid: bkid, token: localStorage.getItem('authToken')
    };
    console.log(info);
    this.http.post('http://127.0.0.1:5000/deletebuyorder', info)
        .subscribe((response)=>{
      this.returnMsg=response["msg"];
      alert(this.returnMsg)
      window.location.reload();
    });
  }

//avatar update section
profilepic : string;
urllink : string;
selectedFile: File = null;
  selectFiles(event){
    if(event.target.files){
      var reader = new FileReader()
      reader.readAsDataURL(event.target.files[0])
      reader.onload = (event:any)=>{
        this.urllink = event.target.result
      }
      this.selectedFile = <File>event.target.files[0];
    }
  }
  avatarChange(event)
  {
    event.preventDefault();
    const target = event.target;
    const fd = new FormData();
    fd.append('file', this.selectedFile, this.selectedFile.name);

    this.http.post('http://127.0.0.1:5000/uploadFile', fd)
      .subscribe((response)=>
      {
        console.log(response);
      });

    var newAva = {
      ava : this.selectedFile.name,
      token : localStorage.getItem('authToken')
    }
    this.http.post('http://127.0.0.1:5000/changeava', newAva)
    .subscribe((response)=>
    { 
      alert(response["msg"]);
    });
  }
// end of avatar update


  userChangePass(event) {
    event.preventDefault();
    const target = event.target;
    const oldpass = target.querySelector('#oldpassword').value;
    const pass1 = target.querySelector('#password1').value;
    const pass2 = target.querySelector('#password2').value;
    console.log(localStorage.getItem('authToken') + 'log')
    var info = {
      oldp: oldpass, p1: pass1, p2: pass2, token: localStorage.getItem('authToken'), user: this.usern
    };
    console.log(info);
    
    this.http.post('http://127.0.0.1:5000/changepass', info)
        .subscribe((response)=>{
      this.returnMsg=response["msg"];
      console.log(this.returnMsg);
    });
  }
}
