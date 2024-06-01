/**
 * @id java-kotlin/import-static
 * @name Import
 * @description Import Static Member
 * @kind problem
 * @problem.severity recommendation
 */

import java

from ImportStaticTypeMember i
select i, i.getFile().getRelativePath() + " " + i.getAMemberImport().getQualifiedName()