using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

using Amazon.DynamoDBv2.DocumentModel;
using Amazon.DynamoDBv2;

using CartelBotAPI.Models;
using CartelBotAPI.Services;

using Newtonsoft.Json.Linq;
using Newtonsoft.Json;

namespace CartelBotAPI.Controllers
{
    [Route("cartelbot")]
    [ApiController]
    public class DefaultController : ControllerBase
    {
        [Route("add")]
        [HttpGet]
        public async Task<IActionResult> add([FromQuery]string name, [FromQuery]string key, [FromQuery]string secret) //bitmex - btc only for now
        {
            // if empty params bad request
            try
            {
                if (string.IsNullOrEmpty(name) || string.IsNullOrEmpty(key) || string.IsNullOrEmpty(secret))
                {
                    return BadRequest("missing params");
                }

                try
                {
                    AmazonDynamoDBClient amazonDynamoDB = new AmazonDynamoDBClient();
                    Table table = Table.LoadTable(amazonDynamoDB, "CartelBotRegistry");

                    Document doc = new Document();
                    doc["Name"] = name;
                    doc["Key"] = key;
                    doc["Secret"] = secret;
                    doc["Exchange"] = "bitmex";

                    await table.PutItemAsync(doc);

                    return Content($"success adding: {name}", "application/json");
                }
                catch
                {
                    return BadRequest("error connecting to database");
                }
            }
            catch
            {
                return BadRequest("something went wrong");
            }
        }

        [Route("position")]
        [HttpGet]
        public async Task<IActionResult> position([FromQuery]string name) //only bitcoin position for now
        {
            try
            {
                if(string.IsNullOrEmpty(name))
                {
                    return BadRequest("missing params");
                }

                Document doc = new Document();
                string positionjson;

                try
                {
                    AmazonDynamoDBClient amazonDynamoDB = new AmazonDynamoDBClient();
                    Table table = Table.LoadTable(amazonDynamoDB, "CartelBotRegistry");

                    doc = await table.GetItemAsync(name);
                }
                catch
                {
                    return BadRequest("error finding name");
                }

                BitmexPositionModel model = new BitmexPositionModel();
                BitMEXApi bitmex = new BitMEXApi(doc["Key"], doc["Secret"]);

                try
                {
                    positionjson = await bitmex.getPosition();
                }
                catch
                {
                    return BadRequest("error connecting to bitmex");
                }

                try
                {
                    model = JsonConvert.DeserializeObject<BitmexPositionModel>(positionjson);
                }
                catch
                {
                    return BadRequest("error parsing data");
                }

                PositionResponse response = new PositionResponse();
                response.name = name;
                response.position = model.Position[0].currentQty;
                response.entry = model.Position[0].avgEntryPrice;

                string responsejson = JsonConvert.SerializeObject(response);

                return Content(responsejson, "application/json");
            }
            catch
            {
                return BadRequest("something went wrong");
            }
        }

        [Route("remove")]
        [HttpGet]
        public async Task<IActionResult> remove([FromQuery]string name)
        {
            try
            {
                return BadRequest("not implemented");
            }
            catch
            {
                return BadRequest("not implemented");
            }
        }
    }
}
