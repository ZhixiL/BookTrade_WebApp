import { EventEmitterService } from './../Services/event-emitter.service';
import { buyOrderPost } from './../model';
import { RestService } from './../Services/rest.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-buylist',
  templateUrl: './buy-list.component.html',
  styleUrls: ['./buy-list.component.css']
})
export class BuyListComponent implements OnInit {

  constructor(
    private rs : RestService,
    private ees : EventEmitterService,
    ) { }

  buyOrders : buyOrderPost[] = [];
  searchFilteredTXBK : buyOrderPost[] = [];
  constTXBK : buyOrderPost[] = []; //permanently hold buyorders for the session, in case if buyOrders is manipulated.
  initial : number = 0;
  final : number = 16;
  pageNums;

  ngOnInit()
  {
    if (this.ees.searchSubsVar==undefined) {    
      this.ees.searchSubsVar = this.ees.
      invokeSearch.subscribe((name:string) => {    
        this.searchFor(this.ees.key);
      }); 
    }
    this.rs.readBuyOrderAll()
    .subscribe
      (
        (response) => 
        {
          this.constTXBK = this.buyOrders = response[0]["bookdatas"];
          console.log(this.constTXBK);
          this.pageNums = Array(Math.ceil(response[0]["bookdatas"].length/16)).fill(0).map((x,i)=>i);
        },
        (error) =>
        {
          console.log("No Data Found" + error);
        }
      )
  }
  
  searchFor(key)
  {
    this.buyOrders=this.constTXBK;
    if(key!="")
    {
      this.buyOrders = this.buyOrders.filter((a) => a.bookname.includes(key));
      this.searchFilteredTXBK=this.buyOrders;
    }
    this.pageNums = Array(Math.ceil(this.buyOrders.length/16)).fill(0).map((x,i)=>i);
  }

  pageChange(pgNum)
  {
    this.initial = pgNum*16;
    this.final = (pgNum+1)*16;
  }

  selectChangeHandler (event: any) {
    if(this.searchFilteredTXBK.length==0)
      this.buyOrders=this.constTXBK; //repair the textbook, then filter.
    else
      this.buyOrders=this.searchFilteredTXBK;
    if(event.target.value != "All")//only filter when user selected specific college.
      this.buyOrders = this.buyOrders.filter((a) => a.college == event.target.value)
    this.pageNums = Array(Math.ceil(this.buyOrders.length/16)).fill(0).map((x,i)=>i);
  }

  selectStatus (event: any) {
    if(this.searchFilteredTXBK.length==0)
      this.buyOrders=this.constTXBK; //repair the textbook, then filter.
    else
      this.buyOrders=this.searchFilteredTXBK;
    if(event.target.value != "All")//only filter when user selected specific college.
      this.buyOrders = this.buyOrders.filter((a) => a.stat == event.target.value)
    this.pageNums = Array(Math.ceil(this.buyOrders.length/16)).fill(0).map((x,i)=>i);
  }

  //these variables used to keep track wether or not reverse sort.
  tmCount:number = 0; nmCount:number =0; prCount:number =0;
  sort(choice : number)
  {
    switch(choice){
      case 0:{ //sort by time posted
        this.tmCount++;
        if(this.tmCount%2==1){
          this.buyOrders.sort((a,b) => a.time.localeCompare(b.time));}
        else{
          this.buyOrders.sort((a,b) => b.time.localeCompare(a.time));}
        break;
      }case 1:{ //sort by bookname
        this.nmCount++;
        if(this.nmCount%2==1){
          this.buyOrders.sort((a,b) => a.bookname.localeCompare(b.bookname));}
        else{
          this.buyOrders.sort((a,b) => b.bookname.localeCompare(a.bookname));}
        break;
      }case 2:{ //sort by price
        this.prCount++;
        if(this.prCount%2==1){
        this.buyOrders.sort((a,b) => a.price - b.price);}
        else{
          this.buyOrders.sort((a,b) => b.price - a.price);}
        break;
      }
    }
  }
}
