import { Textbook } from './../model';
import { RestService } from './../Services/rest.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-booklist',
  templateUrl: './booklist.component.html',
  styleUrls: ['./booklist.component.css']
})
export class BooklistComponent implements OnInit {

  constructor(private rs : RestService) { }

  textbooks : Textbook[] = [];
  constTXBK : Textbook[] = []; //permanently hold textbooks for the session, in case if textbooks is manipulated.
  initial : number = 0;
  final : number = 16;
  pageNums;

  ngOnInit()
  {
    this.rs.readTextbookAll()
    .subscribe
      (
        (response) => 
        {
          this.constTXBK = this.textbooks = response[0]["bookdata"];
          this.pageNums = Array(Math.ceil(response[0]["bookdata"].length/16)).fill(0).map((x,i)=>i);
        },
        (error) =>
        {
          console.log("No Data Found" + error);
        }
      )
    
  }
  
  pageChange(pgNum)
  {
    this.initial = pgNum*16;
    this.final = (pgNum+1)*16
  }

  selectChangeHandler (event: any) {
    this.textbooks=this.constTXBK; //repair the textbook, then filter.
    if(event.target.value != "All")//only filter when user selected specific college.
      this.textbooks = this.textbooks.filter((a) => a.college == event.target.value)
    this.pageNums = Array(Math.ceil(this.textbooks.length/16)).fill(0).map((x,i)=>i);
  }

  //these variables used to keep track wether or not reverse sort.
  tmCount:number = 0; nmCount:number =0; prCount:number =0;
  sort(choice : number)
  {
    switch(choice){
      case 0:{ //sort by time posted
        this.tmCount++;
        if(this.tmCount%2==1){
          this.textbooks.sort((a,b) => a.time.localeCompare(b.time));}
        else{
          this.textbooks.sort((a,b) => b.time.localeCompare(a.time));}
        break;
      }case 1:{ //sort by bookname
        this.nmCount++;
        if(this.nmCount%2==1){
          this.textbooks.sort((a,b) => a.bookname.localeCompare(b.bookname));}
        else{
          this.textbooks.sort((a,b) => b.bookname.localeCompare(a.bookname));}
        break;
      }case 2:{ //sort by price
        this.prCount++;
        if(this.prCount%2==1){
        this.textbooks.sort((a,b) => a.price - b.price);}
        else{
          this.textbooks.sort((a,b) => b.price - a.price);}
        break;
      }
    }
  }
}
