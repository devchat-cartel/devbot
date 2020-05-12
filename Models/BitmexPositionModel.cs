
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;


namespace CartelBotAPI.Models
{
    public class BitmexPositionModel
    {
        public Class1[] Position { get; set; }
    }

    public class Class1
    {
        public int account { get; set; }
        public string symbol { get; set; }
        public string currency { get; set; }
        public string underlying { get; set; }
        public string quoteCurrency { get; set; }
        public int commission { get; set; }
        public int initMarginReq { get; set; }
        public int maintMarginReq { get; set; }
        public int riskLimit { get; set; }
        public int leverage { get; set; }
        public bool crossMargin { get; set; }
        public int deleveragePercentile { get; set; }
        public int rebalancedPnl { get; set; }
        public int prevRealisedPnl { get; set; }
        public int prevUnrealisedPnl { get; set; }
        public int prevClosePrice { get; set; }
        public DateTime openingTimestamp { get; set; }
        public int openingQty { get; set; }
        public int openingCost { get; set; }
        public int openingComm { get; set; }
        public int openOrderBuyQty { get; set; }
        public int openOrderBuyCost { get; set; }
        public int openOrderBuyPremium { get; set; }
        public int openOrderSellQty { get; set; }
        public int openOrderSellCost { get; set; }
        public int openOrderSellPremium { get; set; }
        public int execBuyQty { get; set; }
        public int execBuyCost { get; set; }
        public int execSellQty { get; set; }
        public int execSellCost { get; set; }
        public int execQty { get; set; }
        public int execCost { get; set; }
        public int execComm { get; set; }
        public DateTime currentTimestamp { get; set; }
        public int currentQty { get; set; }
        public int currentCost { get; set; }
        public int currentComm { get; set; }
        public int realisedCost { get; set; }
        public int unrealisedCost { get; set; }
        public int grossOpenCost { get; set; }
        public int grossOpenPremium { get; set; }
        public int grossExecCost { get; set; }
        public bool isOpen { get; set; }
        public int markPrice { get; set; }
        public int markValue { get; set; }
        public int riskValue { get; set; }
        public int homeNotional { get; set; }
        public int foreignNotional { get; set; }
        public string posState { get; set; }
        public int posCost { get; set; }
        public int posCost2 { get; set; }
        public int posCross { get; set; }
        public int posInit { get; set; }
        public int posComm { get; set; }
        public int posLoss { get; set; }
        public int posMargin { get; set; }
        public int posMaint { get; set; }
        public int posAllowance { get; set; }
        public int taxableMargin { get; set; }
        public int initMargin { get; set; }
        public int maintMargin { get; set; }
        public int sessionMargin { get; set; }
        public int targetExcessMargin { get; set; }
        public int varMargin { get; set; }
        public int realisedGrossPnl { get; set; }
        public int realisedTax { get; set; }
        public int realisedPnl { get; set; }
        public int unrealisedGrossPnl { get; set; }
        public int longBankrupt { get; set; }
        public int shortBankrupt { get; set; }
        public int taxBase { get; set; }
        public int indicativeTaxRate { get; set; }
        public int indicativeTax { get; set; }
        public int unrealisedTax { get; set; }
        public int unrealisedPnl { get; set; }
        public int unrealisedPnlPcnt { get; set; }
        public int unrealisedRoePcnt { get; set; }
        public int simpleQty { get; set; }
        public int simpleCost { get; set; }
        public int simpleValue { get; set; }
        public int simplePnl { get; set; }
        public int simplePnlPcnt { get; set; }
        public int avgCostPrice { get; set; }
        public int avgEntryPrice { get; set; }
        public int breakEvenPrice { get; set; }
        public int marginCallPrice { get; set; }
        public int liquidationPrice { get; set; }
        public int bankruptPrice { get; set; }
        public DateTime timestamp { get; set; }
        public int lastPrice { get; set; }
        public int lastValue { get; set; }
    }

}
