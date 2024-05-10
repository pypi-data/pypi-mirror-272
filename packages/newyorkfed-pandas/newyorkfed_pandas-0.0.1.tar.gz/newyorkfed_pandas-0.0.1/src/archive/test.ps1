
$date = '2020-01-01'

$result = Invoke-RestMethod ('https://markets.newyorkfed.org/api/rp/reverserepo/propositions/search.json?startDate={0}' -f $date)

$result.repo.operations | Select-Object -First 200 | ft *

$result.repo.operations[-1].propositions


$result_csv = Invoke-RestMethod ('https://markets.newyorkfed.org/api/rp/reverserepo/propositions/search.csv?startDate={0}' -f $date)

$result_csv | ConvertFrom-Csv | Select-Object -First 100 | Format-Table *

$data = $result_csv | ConvertFrom-Csv

$data[-1]