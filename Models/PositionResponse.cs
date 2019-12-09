using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace CartelBotAPI.Models
{
    public class PositionResponse
    {
        public long position { get; set; }
        public float entry { get; set; }
        public string name { get; set; }
    }
}
