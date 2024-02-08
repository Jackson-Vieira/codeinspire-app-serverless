import { DynamoDBClient} from "@aws-sdk/client-dynamodb";
import { ScanCommand, DynamoDBDocumentClient } from "@aws-sdk/lib-dynamodb";

function getLastSunday(){
    const currentDate = new Date();
    const currentDayOfWeek = currentDate.getDay(); // 0 Domingo, 1 Segunda, ...
    const daysToSubtract = (currentDayOfWeek + 7) % 7;
    const lastSundayDate = new Date(currentDate);
    lastSundayDate.setDate(currentDate.getDate() - daysToSubtract);
    return lastSundayDate;
};

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

async function getTips(event){

    const lastSundayFormated = getLastSunday().toISOString().split("T")[0];

    const command = new ScanCommand({
        TableName: process.env.DYNAMODB_TABLE_NAME,
        FilterExpression: "tip_date >= :lastSunday",
        ExpressionAttributeValues: {
             ":lastSunday": lastSundayFormated
    }});

    const response = await docClient.send(command);
    const tips = response.Items;

    return {
        statusCode: 200,
        body: JSON.stringify(tips)
    };
};

export const handler = getTips;